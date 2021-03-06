from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    core,
)


class HitCounter(core.Construct):

    @property
    def handler(self):
        return self._handler

    def __init__(self, scope: core.Construct, id: str, downstream: _lambda.IFunction, **kwargs):
        super().__init__(scope, id, **kwargs)

        table = ddb.Table(
            self, 'Hits',
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING}
        )

        self._handler = _lambda.Function(
            self, 'HitCountHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='hit_counter.handler',
            code=_lambda.Code.from_asset('lam'),
            environment={
                'DOWNSTREAM_FUNCTION_NAME': downstream.function_name,
                'HITS_TABLE_NAME': table.table_name,
            }
        )

        # NEED TO GIVE PERMISSIONS FOR DYNAMO AND LAMBDA
        table.grant_read_write_data(self.handler)
        downstream.grant_invoke(self.handler)
