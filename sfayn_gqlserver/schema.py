import graphene
from ddd.order_management.entrypoints.graphql import queries, mutations



class Query(
    queries.ListShippingOptionsQuery,
    queries.ListCustomerAddressesQuery,
    queries.GetOrderQuery
):
    pass

class Mutation(graphene.ObjectType):

    add_order = mutations.add_shipment_mutation.AddOrderMutation.Field()
    add_shipment = mutations.add_shipment_mutation.AddShipmentMutation.Field()
    confirm_shipment = mutations.confirm_shipment_mutation.ConfirmShipmentMutation.Field()
    deliver_shipment = mutations.deliver_shipment_mutation.DeliverShipmentMutation.Field()
    cancel_order = mutations.cancel_order_mutation.CancelOrderMutation.Field()
    mark_as_completed_order = mutations.mark_as_completed_mutation.MarkAsCompletedMutation.Field()

    request_return = mutations.request_return_mutation.RequestReturnMutation.Field()
    process_refund = mutations.process_refund_mutation.ProcessRefundMutation.Field()
    escalate_reviewer = mutations.escalate_reviewer_mutation.EscalateReviewerMutation.Field()
    review_order = mutations.review_order_mutation.ReviewOrderMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

