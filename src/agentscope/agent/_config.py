# -*- coding: utf-8 -*-
"""The agent config classes.

本模块集中定义 AgentScope 中与智能体运行相关的配置模型。
这些模型基于 Pydantic，既用于运行时参数校验，也可通过
``Field`` 元数据生成面向配置界面或文档的 JSON Schema。
"""

from pydantic import BaseModel, Field

from ..model import ChatModelBase


class SummarySchema(BaseModel):
    """The compressed memory model, used to generate summary of old memories.

    旧上下文被压缩时使用的结构化摘要模型。每个字段都会约束摘要中
    必须保留的信息类型，确保压缩后的内容足够支撑后续继续完成任务。
    """

    task_overview: str = Field(
        # description 中文说明：
        # 记录用户的核心诉求、验收标准，以及用户明确提出的约束或澄清。
        # 该字段帮助后续上下文快速恢复“这件事到底要完成什么”。
        description=(
            "The user's core request and success criteria.\n"
            "Any clarifications or constraints they specified"
        ),
    )
    current_state: str = Field(
        # description 中文说明：
        # 记录当前已经完成的工作、涉及的文件路径，以及已经产出的结果或工件。
        # 该字段帮助后续执行者了解任务进度，避免重复分析或重复修改。
        description=(
            "What has been completed so far.\n"
            "File created, modified, or analyzed (with paths if relevant).\n"
            "Key outputs or artifacts produced."
        ),
    )
    important_discoveries: str = Field(
        # description 中文说明：
        # 记录过程中发现的技术限制、需求细节、关键决策及原因。
        # 如果遇到错误、已尝试但失败的方案，也应写入这里，避免后续重蹈覆辙。
        description=(
            "Technical constraints or requirements uncovered.\n"
            "Decisions made and their rationale.\n"
            "Errors encountered and how they were resolved.\n"
            "What approaches were tried that didn't work (and why)"
        ),
    )
    next_steps: str = Field(
        # description 中文说明：
        # 记录为了完成任务还需要继续执行的具体动作、阻塞点或开放问题。
        # 当剩余事项不止一个时，应写清楚优先级，方便恢复后直接继续推进。
        description=(
            "Specific actions needed to complete the task.\n"
            "Any blockers or open questions to resolve.\n"
            "Priority order if multiple steps remain"
        ),
    )
    context_to_preserve: str = Field(
        # description 中文说明：
        # 记录跨压缩周期必须长期保留的上下文，例如用户偏好、领域知识、
        # 特殊风格要求，以及曾向用户承诺过的事项。
        description=(
            "User preferences or style requirements.\n"
            "Domain-specific details that aren't obvious.\n"
            "Any promises made to the user"
        ),
    )
    """The important context to preserve across compression, e.g. user
    preferences, domain-specific details and promises made to the user."""


class ContextConfig(BaseModel):
    """The context related configuration in AgentScope.

    AgentScope 中与上下文管理和上下文压缩相关的配置。
    当对话或记忆接近模型上下文上限时，这些参数决定何时触发压缩、
    压缩时保留多少原始内容，以及压缩摘要的生成与展示格式。
    """

    model_config = {"arbitrary_types_allowed": True}
    """Allow arbitrary types in the pydantic model."""

    trigger_ratio: float = Field(default=0.8, gt=0, lt=0.9)
    """When the token exceeds this ratio of the maximum context length, the
    context will be compressed. To reserve the context for context compression,
    the maximum ratio is 0.9."""

    reserve_ratio: float = Field(default=0.1, gt=0, lt=0.9)
    """The ratio of the tokens to reserve in context compression, which should
    be smaller than the trigger ratio."""

    compression_prompt: str = Field(
        default=(
            # 中文说明：
            # 这段提示词会告诉压缩模型：当前任务尚未完成，需要生成一份
            # 可在未来上下文窗口中继续接力的摘要。摘要应结构化、简洁、
            # 可执行，避免只做泛泛而谈的聊天总结。
            "<system-hint>You have been working on the task described above "
            "but have not yet completed it. "
            "Now write a continuation summary that will allow you to resume "
            "work efficiently in a future context window where the "
            "conversation history will be replaced with this summary. "
            "Your summary should be structured, concise, and actionable."
            "</system-hint>"
        ),
        # ``format: textarea`` is a hint for schema-driven UI renderers
        # to use a multi-line input. Plain JSON Schema doesn't natively
        # express this, so we piggy-back on ``json_schema_extra``.
        json_schema_extra={"format": "textarea"},
    )
    """The prompt used to guide the compression model to generate the
    compressed summary, which will be wrapped into a user message and
    attach to the end of the current memory."""

    summary_template: str = Field(
        default=(
            # 中文说明：
            # 这是注入给智能体阅读的摘要模板。模板中的占位符来自
            # ``SummarySchema``，会按任务概览、当前状态、重要发现、
            # 下一步和需保留上下文的顺序组织压缩结果。
            "<system-info>Here is a summary of your previous work\n"
            "# Task Overview\n"
            "{task_overview}\n\n"
            "# Current State\n"
            "{current_state}\n\n"
            "# Important Discoveries\n"
            "{important_discoveries}\n\n"
            "# Next Steps\n"
            "{next_steps}\n\n"
            "# Context to Preserve\n"
            "{context_to_preserve}"
            "</system-info>"
        ),
        json_schema_extra={"format": "textarea"},
    )
    """The string template to present the compressed summary to the agent,
    which will be formatted with the fields from the
    `summary_schema`."""

    summary_schema: dict = Field(
        default_factory=SummarySchema.model_json_schema,
    )
    """The structured model used to guide the agent to generate the
    structured compressed summary."""

    tool_result_limit: int = Field(
        title="Tool Result Limit",
        default=50000,
        # description 中文说明：
        # 工具调用结果允许保留的最大 token 长度。超过该限制时，
        # 工具结果会被截断，以防止单次工具输出撑爆上下文窗口。
        description=(
            "The maximum length of the tool results in tokens. "
            "If exceeded, the tool result will be truncated."
        ),
    )
    """The tool result limit to avoid tool result bursting."""


class ReActConfig(BaseModel):
    """The reasoning related configuration.

    与 ReAct（Reasoning + Acting，推理与行动交替）循环相关的配置。
    这些参数控制智能体单次回复中最多执行多少轮“思考-调用工具”，
    以及工具调用被拒绝或用户打断时应该如何处理。
    """

    max_iters: int = Field(
        title="Max Iterations",
        default=20,
        # description 中文说明：
        # 单次回复中允许执行的最大推理-行动迭代次数。
        # 该限制用于避免智能体在一次回复内无限循环调用工具。
        description="The maximum number of reasoning-acting iterations in "
        "one reply",
    )
    """The maximum number of iterations for the reasoning-acting loop."""

    stop_on_reject: bool = Field(
        title="Rejection Handling",
        default=False,
        # description 中文说明：
        # 当工具执行请求被外部拒绝时，是否立即停止继续回复。
        # 若为 True，智能体会等待用户或外部系统进一步交互。
        description="Whether to stop replying when being rejected to "
        "execute tools.",
    )
    """If stop reasoning when tool call(s) are rejected. If `True`, the agent
    won't continue reasoning and wait for outside interaction from the user.
    """

    interruption_message: str = Field(
        title="Interruption Message",
        default="I notice the interruption. How can I help you?",
        # description 中文说明：
        # 用户或系统打断当前执行时返回的快速回复文本。
        # 该消息用于确认已经感知到打断，并把控制权交回给用户。
        description="The quick reply message when interrupted.",
    )
    """The interruption message."""

    interruption_raise_cancelled_error: bool = Field(
        title="Raise CancelledError on Interruption",
        default=False,
        # description 中文说明：
        # 控制打断处理完成后是否重新抛出 ``asyncio.CancelledError``。
        # 为 False 时，取消异常会在生成打断上下文后被吞掉；
        # 为 True 时，异常会继续向上冒泡，交给外层调用方处理。
        description="Whether to re-raise ``asyncio.CancelledError`` after "
        "handling the interruption. When ``False``, the ``CancelledError`` "
        "is swallowed once the interruption context has been produced.",
    )
    """Whether to re-raise the ``asyncio.CancelledError`` after the
    interruption has been handled. When ``False``, the ``CancelledError``
    is swallowed once the fallback interruption message and
    ``ReplyEndEvent`` have been emitted."""


class ModelConfig(BaseModel):
    """The model related configuration.

    与底层聊天模型调用相关的配置，主要覆盖失败重试次数以及主模型失败时
    使用的备用模型。这里的重试语义需要与 ``ChatModelBase`` 保持一致。
    """

    # TODO: remove this line after PR #1564 is merged, where the ChatModel
    #  will be child class of BaseModel
    model_config = {"arbitrary_types_allowed": True}

    max_retries: int = Field(
        default=0,
        ge=0,
        # description 中文说明：
        # 在首次调用失败后、切换到备用模型之前，额外重试主模型的次数。
        # ``0`` 表示只调用一次主模型，失败后立即进入 fallback 流程。
        # 默认值设为 0，是为了避免与模型内部自带的重试机制叠加。
        description=(
            "Number of retries on top of the initial call before falling "
            "over to the fallback model. ``0`` means call the model exactly "
            "once and immediately move to the fallback on failure. Same "
            "semantics as ``ChatModelBase.max_retries``. Defaults to 0 to "
            "avoid compounding with the model's own inner retry loop."
        ),
    )
    """Number of retries on top of the initial call before falling over to
    the fallback model. ``0`` means a single attempt with no retries.
    Mirrors the semantics of ``ChatModelBase.max_retries``."""

    fallback_model: ChatModelBase | None = Field(
        default=None,
        # description 中文说明：
        # 主模型调用失败时使用的备用模型。它同样参与 ``max_retries``
        # 所描述的失败转移逻辑。
        description="The fallback model used when the main model fails.",
    )
    """The fallback model used when the main model fails. Also supports the
    max_retries logic."""
