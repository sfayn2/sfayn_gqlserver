

def get_command_handlers(commands, handlers, uow, access_control):
    return {
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