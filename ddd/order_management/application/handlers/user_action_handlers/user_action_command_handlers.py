

def get_command_handlers(commands, handlers, application_services, tenant_service):
    return {
        commands.EscalateReviewerCommand: lambda command, **deps: handlers.handle_escalate_reviewer(
            command=command,
            **deps
        ),
        commands.ReviewOrderCommand: lambda command, **deps: handlers.handle_review_order(
            command=command,
            **deps
        ),
        commands.RequestReturnCommand: lambda command, **deps: handlers.handle_request_return(
            command=command,
            **deps
        ),
        commands.ProcessRefundCommand: lambda command, **deps: handlers.handle_process_refund(
            command=command,
            refund_service=application_services.RefundService(
                uow=repositories.DjangoOrderUnitOfWork(),
                tenant_service=tenant_service,
                user_action_service=user_action_service
            ),
            **deps
        ),
    }