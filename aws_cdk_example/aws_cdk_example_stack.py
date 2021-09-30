from aws_cdk import (
    core as cdk,
    aws_lambda as _lambda,
    aws_apigateway as apigw
)

from .aws_hit_counter import HitCounter


class AwsCdkExampleStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lam'),
            handler='hello_lambda.handler',
        )
        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=my_lambda,
        )
        apigw.LambdaRestApi(
            self, 'Endpoint',
            # handler=my_lambda,
            handler=hello_with_counter.handler,
        )
