import os
from string import Template
import requests
from ethereum_connection import EthereumConnection
from .interface_blocklogs_service import IBlockLogsService


class GraphQLService(IBlockLogsService):
    def __init__(self):
        self.__eth = EthereumConnection(os.environ.get("URL_NODE"))
        self.__url_block_service = os.environ.get("URL_BLOCK_SERVICE")

    def __query_builder(self, filter_params=None):
        query_template = Template("""{
            blocks $filter_params {
            number
            hash
            parentHash
            timestamp
            logs {
                address
                blockHash
                blockNumber
                data
                topic0
                topic1
                topic2
                topic3
                transactionHash
                }
            }
        }
        """)

        if filter_params is None:
            filter_params = "(first:32)"

        return query_template.substitute(filter_params=filter_params)

    def get_last_nth_blocks(self, num):
        params = '(first:{})'.format(num)

        query = self.__query_builder(params)
        blocks = self.__run_graphql_query(query)

        return blocks

    def get_range_blocks(self, from_block, to_block):
        params = '(number__gte:"{}", number__lte:"{}")'.format(
            from_block,
            to_block
        )

        query = self.__query_builder(params)
        blocks = self.__run_graphql_query(query)

        return blocks

    def __run_graphql_query(self, query):
        url = self.__url_block_service
        querystring = {"query": query}
        response = requests.get(url, params=querystring)
        if response.ok:
            return response.json().get("data").get("blocks")
        else:
            # throw requests exception
            print("RESPONSE NOT OK. REASON: {}".format(response.text))

    @property
    def last_block_mined(self):
        return self.__eth.w3.eth.blockNumber
