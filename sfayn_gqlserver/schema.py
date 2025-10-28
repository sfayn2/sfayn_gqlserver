import graphene
from ddd.order_management.presentation.graphql import queries, mutations



class Query(
    queries.ListShippingOptionsQuery,
    queries.ListCustomerAddressesQuery,
    queries.GetOrderQuery
):
    pass

class Mutation(graphene.ObjectType):
    add_line_items = mutations.add_line_items_mutation.AddLineItemsMutation.Field()

    add_shipment = mutations.add_shipment_mutation.AddShipmentMutation.Field()
    ship_shipment = mutations.ship_shipment_mutation.ShipShipmentMutation.Field()
    add_shipping_tracking_reference = mutations.add_shipping_tracking_reference_mutation.AddShippingTrackingReferenceMutation.Field()
    deliver_shipment = mutations.deliver_shipment_mutation.DeliverShipmentMutation.Field()
    cancel_order = mutations.cancel_order_mutation.CancelOrderMutation.Field()
    mark_as_completed_order = mutations.mark_as_completed_mutation.MarkAsCompletedMutation.Field()

    request_return = mutations.request_return_mutation.RequestReturnMutation.Field()
    process_refund = mutations.process_refund_mutation.ProcessRefundMutation.Field()
    escalate_reviewer = mutations.escalate_reviewer_mutation.EscalateReviewerMutation.Field()
    review_order = mutations.review_order_mutation.ReviewOrderMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

