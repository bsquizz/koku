#
# Copyright 2022 Red Hat Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""Views for Masu sources API."""
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters import BooleanFilter
from django_filters import FilterSet
from django_filters import UUIDFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.serializers import UUIDField
from rest_framework.serializers import ValidationError

from api.common.filters import CharListFilter
from api.provider.models import Sources
from masu.api.sources.serializers import SourceSerializer

MIXIN_LIST = [mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet]
HTTP_METHOD_LIST = ["get", "head"]


class SourceFilter(FilterSet):
    """Source custom filters."""

    name = CharListFilter(field_name="name", lookup_expr="name__icontains")
    type = CharListFilter(field_name="source_type", lookup_expr="source_type__icontains")
    account_id = CharListFilter(field_name="account_id", lookup_expr="account_id__icontains")
    schema_name = CharListFilter(
        field_name="provider__customer__schema_name", lookup_expr="provider__customer__schema_name__icontains"
    )
    ocp_on_cloud = BooleanFilter(field_name="provider__infrastructure_id", lookup_expr="isnull", exclude=True)
    infrastructure_provider_id = UUIDFilter(field_name="provider__infrastructure__infrastructure_provider_id")
    cluster_id = CharListFilter(
        field_name="authentication__credentials__cluster_id",
        lookup_expr="authentication__credentials__cluster_id__icontains",
    )
    active = BooleanFilter(field_name="provider__active")
    paused = BooleanFilter(field_name="provider__paused")
    pending_delete = BooleanFilter(field_name="pending_delete")
    pending_update = BooleanFilter(field_name="pending_update")
    out_of_order_delete = BooleanFilter(field_name="out_of_order_delete")

    class Meta:
        model = Sources
        fields = [
            "source_type",
            "name",
            "account_id",
            "schema_name",
            "ocp_on_cloud",
            "infrastructure_provider_id",
            "cluster_id",
            "active",
            "paused",
            "pending_delete",
            "pending_update",
            "out_of_order_delete",
        ]


class SourcesViewSet(*MIXIN_LIST):
    """Source View class."""

    queryset = Sources.objects.all()
    serializer_class = SourceSerializer
    lookup_fields = ("source_id", "source_uuid")
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SourceFilter
    http_method_names = HTTP_METHOD_LIST

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        pk = self.kwargs.get("pk")
        try:
            uuid = UUIDField().to_internal_value(data=pk)
            obj = Sources.objects.get(source_uuid=uuid)
            if obj:
                return obj
        except (ValidationError, Sources.DoesNotExist):
            pass

        try:
            int(pk)
            obj = get_object_or_404(queryset, **{"pk": pk})
            self.check_object_permissions(self.request, obj)
        except ValueError:
            raise Http404

        return obj
