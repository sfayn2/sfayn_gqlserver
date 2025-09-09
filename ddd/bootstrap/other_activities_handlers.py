from ddd.order_management.application import (
    commands, 
)

COMMAND_HANDLERS = {
    commands.EscalateReviewerCommand: lambda command, **deps: handlers.handle_escalate_reviewer(
        command=command,
        uow=repositories.DjangoOrderUnitOfWork(),
        access_control=access_control,
        **deps
    ),
    commands.ReviewOrderCommand: lambda command, **deps: handlers.handle_review_order(
        command=command,
        uow=repositories.DjangoOrderUnitOfWork(),
        access_control=access_control,
        **deps
    ),
}