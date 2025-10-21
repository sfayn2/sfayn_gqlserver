import graphene
from graphene import relay
from graphene.types.generic import GenericScalar
from ddd.order_management.application import (
    message_bus, commands
  )
from ddd.order_management.presentation.graphql import object_types, common
from ddd.order_management.infrastructure import (
    access_control1,
)


# ==========================
# Mutations 
# ===================
class ReviewOrderMutation(relay.ClientIDMutation):
    class Input:
        order_id = graphene.String(required=True)
        is_approved = graphene.Boolean(required=True)
        comments = graphene.String(required=True)

    result = graphene.Field(object_types.ResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        token = common.get_token_from_context(info)
        user_ctx = access_control1.get_user_context(token)

        command = commands.ReviewOrderCommand.model_validate(input)
        result = message_bus.handle(command, user_ctx=user_ctx)

        return cls(result=object_types.ResponseType(**result.model_dump()))

