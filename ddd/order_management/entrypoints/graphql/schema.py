import graphene
from ddd.order_management.entrypoints.graphql import queries, mutations



class Query(
    queries.GetOrderQuery
):
    pass

class Mutation(graphene.ObjectType):

    add_order = mutations.add_order_mutation.AddOrderMutation.Field()
    add_shipment = mutations.add_shipment_mutation.AddShipmentMutation.Field()
    cancel_shipment = mutations.cancel_shipment_mutation.CancelShipmentMutation.Field()
    confirm_shipment = mutations.confirm_shipment_mutation.ConfirmShipmentMutation.Field()
    deliver_shipment = mutations.deliver_shipment_mutation.DeliverShipmentMutation.Field()
    cancel_order = mutations.cancel_order_mutation.CancelOrderMutation.Field()
    mark_as_completed = mutations.mark_as_completed_mutation.MarkAsCompletedMutation.Field()

    request_return = mutations.RequestReturnMutation.Field()
    process_refund = mutations.ProcessRefundMutation.Field()
    escalate_reviewer = mutations.EscalateReviewerMutation.Field()
    review_order = mutations.ReviewOrderMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

