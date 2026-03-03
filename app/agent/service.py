import json
import re

from openai import AsyncOpenAI

from app.core.config import settings
from app.modules.finance.transactions.model import Transaction
from app.modules.finance.transactions.repo import TransactionRepo
from app.modules.user.model import User
from app.agent.schema import PendingTransaction
from app.agent.tools import TOOLS, execute_tool

CONFIRM_PATTERN = re.compile(r"^(sim|ok|confirmar?|s|yes|✅|👍)$", re.IGNORECASE)
CANCEL_PATTERN = re.compile(r"^(n[aã]o|cancela(r)?|nope|❌|👎)$", re.IGNORECASE)

MAX_TOOL_ROUNDS = 6

SYSTEM_PROMPT = (
    "Você é o Friday Night, assistente financeiro pessoal no Telegram.\n"
    "- Use as ferramentas para buscar contas, tags e métodos de pagamento.\n"
    "- Escolha a opção mais provável automaticamente.\n"
    "- Se ambíguo, pergunte objetivamente (máx 1 pergunta).\n"
    "- Quando tiver tudo, chame SEMPRE `propose_transaction`.\n"
    "- NUNCA registre sem propor primeiro.\n"
    "- Conciso. Português do Brasil. Data padrão: hoje (UTC-3)."
)


class AgentService:
    def __init__(self) -> None:
        self.histories: dict[int, list[dict]] = {}
        self.pending: dict[int, PendingTransaction] = {}
        self._client = AsyncOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )

    async def chat(self, chat_id: int, user_message: str, user: User, db) -> str:
        text = user_message.strip()

        # Confirmation gate (before LLM)
        if chat_id in self.pending:
            pending = self.pending[chat_id]
            if CONFIRM_PATTERN.match(text):
                try:
                    await self._execute_pending(pending, user, db)
                    del self.pending[chat_id]
                    return "✅ Transação registrada com sucesso!"
                except Exception as e:
                    del self.pending[chat_id]
                    return f"❌ Erro ao registrar: {e}"
            elif CANCEL_PATTERN.match(text):
                del self.pending[chat_id]
                return "Cancelado. O que mais posso ajudar?"
            else:
                # Unrecognized — discard pending and treat as new intent
                del self.pending[chat_id]

        # Append user message to history
        history = self.histories.setdefault(chat_id, [])
        history.append({"role": "user", "content": text})

        messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}] + history[-19:]

        # Tool loop
        for _ in range(MAX_TOOL_ROUNDS):
            response = await self._client.chat.completions.create(
                model=settings.AGENT_MODEL,
                messages=messages,
                tools=TOOLS,  # type: ignore[arg-type]
                tool_choice="auto",
            )
            choice = response.choices[0]

            if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
                tool_calls = choice.message.tool_calls

                # Add assistant message with tool calls to context
                assistant_msg: dict = {
                    "role": "assistant",
                    "content": choice.message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in tool_calls
                    ],
                }
                messages.append(assistant_msg)

                # Execute each tool and append results
                for tc in tool_calls:
                    args = json.loads(tc.function.arguments)
                    result = await execute_tool(
                        tc.function.name,
                        args,
                        user,
                        db,
                        chat_id,
                        self.pending,
                    )
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result,
                    })
            else:
                reply = choice.message.content or ""
                history.append({"role": "assistant", "content": reply})
                # Keep history bounded
                if len(history) > 40:
                    self.histories[chat_id] = history[-40:]
                return reply

        return "Desculpe, não consegui processar. Tente novamente."

    async def _execute_pending(
        self, pending: PendingTransaction, user: User, db
    ) -> Transaction:
        t = Transaction(
            user_id=user.id,
            account_id=pending.account_id,
            tag_id=pending.tag_id,
            payment_method_id=pending.payment_method_id,
            currency_id=pending.currency_id,
            value=pending.value,
            description=pending.description,
            date_transaction=pending.date,
        )
        return await TransactionRepo(db).create_update(t)


agent_service = AgentService()
