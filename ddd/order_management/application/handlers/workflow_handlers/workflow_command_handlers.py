

def get_command_handlers(commands, handlers, uow, access_control, workflow_service):
    return {
        commands.EscalateReviewerCommand: lambda command, **deps: handlers.handle_escalate_reviewer(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            access_control=access_control,
            workflow_service=workflow_service
            **deps
        ),
        commands.ReviewOrderCommand: lambda command, **deps: handlers.handle_review_order(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            access_control=access_control,
            workflow_service=workflow_service
            **deps
        ),
        commands.RequestReturnCommand: lambda command, **deps: handlers.handle_request_return(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            access_control=access_control,
            workflow_service=workflow_service
            **deps
        ),
        commands.ProcessRefundCommand: lambda command, **deps: handlers.handle_process_refund(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            access_control=access_control,
            workflow_service=workflow_service
            **deps
        ),
    }