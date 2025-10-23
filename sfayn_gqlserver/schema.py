import graphene
from ddd.order_management.presentation.graphql import queries, mutations



class Query(
    queries.ListShippingOptionsQuery,
    queries.ListCustomerAddressesQuery,
    queries.GetOrderQuery
):
    pass

class Mutation(graphene.ObjectType):
    checkout_items = mutations.checkout_items_mutation.CheckoutItemsMutation.Field()
    change_destination = mutations.change_destination_mutation.ChangeDestinationMutation.Field()
    change_order_quantity = mutations.change_order_quantity_mutation.ChangeOrderQuantityMutation.Field()
    add_line_items = mutations.add_line_items_mutation.AddLineItemsMutation.Field()
    remove_line_items = mutations.remove_line_items_mutation.RemoveLineItemsMutation.Field()
    add_coupon = mutations.add_coupon_mutation.AddCouponMutation.Field()
    remove_coupon = mutations.remove_coupon_mutation.RemoveCouponMutation.Field()
    select_shipping_option = mutations.select_shipping_option_mutation.SelectShippingOptionMutation.Field()
    place_order = mutations.place_order_mutation.PlaceOrderMutation.Field()
    confirm_order = mutations.confirm_order_mutation.ConfirmOrderMutation.Field()
    cancel_order = mutations.cancel_order_mutation.CancelOrderMutation.Field()
    add_shipping_tracking_reference = mutations.add_shipping_tracking_reference_mutation.AddShippingTrackingReferenceMutation.Field()
    mark_as_completed_order = mutations.mark_as_completed_mutation.MarkAsCompletedMutation.Field()
    request_return = mutations.request_return_mutation.RequestReturnMutation.Field()
    process_refund = mutations.process_refund_mutation.ProcessRefundMutation.Field()
    escalate_reviewer = mutations.escalate_reviewer_mutation.EscalateReviewerMutation.Field()
    review_order = mutations.review_order_mutation.ReviewOrderMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

