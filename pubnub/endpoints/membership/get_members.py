import six

from pubnub import utils
from pubnub.endpoints.endpoint import Endpoint
from pubnub.managers import TokenManagerProperties
from pubnub.models.consumer.membership import PNGetMembersResult
from pubnub.enums import HttpMethod, PNOperationType, PNResourceType
from pubnub.exceptions import PubNubException


class GetMembers(Endpoint):
    GET_MEMBERS_PATH = '/v1/objects/%s/spaces/%s/users'
    MAX_LIMIT = 100

    def __init__(self, pubnub):
        Endpoint.__init__(self, pubnub)
        self._start = None
        self._end = None
        self._limit = GetMembers.MAX_LIMIT
        self._count = False
        self._include = None
        self._space_id = None

    def space_id(self, space_id):
        assert isinstance(space_id, six.string_types)
        self._space_id = space_id
        return self

    def start(self, start):
        assert isinstance(start, six.string_types)
        self._start = start
        return self

    def end(self, end):
        assert isinstance(end, six.string_types)
        self._end = end
        return self

    def limit(self, limit):
        assert isinstance(limit, six.integer_types)
        self._limit = limit
        return self

    def count(self, count):
        self._count = bool(count)
        return self

    def include(self, data):
        self._include = data
        return self

    def custom_params(self):
        params = {}

        if self._start is not None:
            params['start'] = self._start

        if self._end is not None and self._start is None:
            params['end'] = self._end

        if self._count is True:
            params['count'] = True

        if self._limit != GetMembers.MAX_LIMIT:
            params['limit'] = self._limit

        if self._include:
            params['include'] = utils.join_items(self._include)

        return params

    def build_path(self):
        if self._space_id is None:
            raise PubNubException('Provide space_id.')
        return GetMembers.GET_MEMBERS_PATH % (self.pubnub.config.subscribe_key, self._space_id)

    def http_method(self):
        return HttpMethod.GET

    def is_auth_required(self):
        return True

    def validate_params(self):
        self.validate_subscribe_key()
        if self._space_id is None:
            raise PubNubException('Provide space_id.')

    def create_response(self, envelope):   # pylint: disable=W0221
        return PNGetMembersResult(envelope)

    def request_timeout(self):
        return self.pubnub.config.non_subscribe_request_timeout

    def connect_timeout(self):
        return self.pubnub.config.connect_timeout

    def operation_type(self):
        return PNOperationType.PNGetMembersOperation

    def name(self):
        return 'Get members'

    def get_tms_properties(self):
        return TokenManagerProperties(
            resource_type=PNResourceType.SPACE,
            resource_id=self._space_id if self._space_id is not None else ""
        )
