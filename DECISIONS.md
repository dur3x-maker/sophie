# Architecture Decision Records

## ADR-001 — Async Pipeline

- ID: ADR-001
- Decision: Внутренний pipeline обработки команд является асинхронным.
- Reason: Интерфейсы, LLM providers и будущие Tools требуют неблокирующего I/O.
- Status: Accepted

## ADR-002 — RuleBasedRouter

- ID: ADR-002
- Decision: Первый Router реализован как rule-based selector.
- Reason: На раннем этапе достаточно простых правил без LLM-зависимости.
- Status: Accepted

## ADR-003 — WorkerFactory

- ID: ADR-003
- Decision: Создание Worker выполняет WorkerFactory.
- Reason: Router возвращает класс Worker, а создание экземпляров вынесено в отдельную точку.
- Status: Accepted

## ADR-004 — Provider Abstraction

- ID: ADR-004
- Decision: LLM providers реализуют общий BaseProvider.
- Reason: OpenRouter, OpenAI, Anthropic, Gemini и другие providers должны заменяться без изменения бизнес-логики.
- Status: Accepted

## ADR-005 — Frozen Architecture

- ID: ADR-005
- Decision: Pipeline и границы слоев считаются замороженными.
- Reason: Стабильная архитектура нужна для предсказуемой разработки возможностей агента.
- Status: Accepted

## ADR-006 — Interfaces to UserCommand

- ID: ADR-006
- Decision: Все interfaces преобразуют входящие данные в UserCommand.
- Reason: CLI, Telegram, API и будущие interfaces должны входить в единый доменный pipeline.
- Status: Accepted

## ADR-007 — LLM Only Through LLMManager

- ID: ADR-007
- Decision: Все обращения к LLM проходят только через LLMManager.
- Reason: Worker не должен зависеть от конкретного provider или внешнего API.
- Status: Accepted
