# Copyright (c) Microsoft. All rights reserved.

from logging import Logger
from unittest.mock import AsyncMock, patch

import pytest

from semantic_kernel.connectors.ai.complete_request_settings import (
    CompleteRequestSettings,
)
from semantic_kernel.connectors.ai.open_ai.services.azure_text_completion import (
    AzureTextCompletion,
)
from semantic_kernel.connectors.ai.open_ai.services.open_ai_text_completion import (
    OpenAITextCompletion,
)


def test_azure_text_completion_init() -> None:
    deployment_name = "test_deployment"
    endpoint = "https://test-endpoint.com"
    api_key = "test_api_key"
    api_version = "2023-03-15-preview"
    logger = Logger("test_logger")

    # Test successful initialization
    azure_text_completion = AzureTextCompletion(
        deployment_name=deployment_name,
        endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
        logger=logger,
    )

    assert azure_text_completion._endpoint == endpoint
    assert azure_text_completion._api_version == api_version
    assert azure_text_completion._api_type == "azure"
    assert isinstance(azure_text_completion, OpenAITextCompletion)


def test_azure_text_completion_init_with_empty_deployment_name() -> None:
    # deployment_name = "test_deployment"
    endpoint = "https://test-endpoint.com"
    api_key = "test_api_key"
    api_version = "2023-03-15-preview"
    logger = Logger("test_logger")

    with pytest.raises(
        ValueError, match="The deployment name cannot be `None` or empty"
    ):
        AzureTextCompletion(
            deployment_name="",
            endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
            logger=logger,
        )


def test_azure_text_completion_init_with_empty_api_key() -> None:
    deployment_name = "test_deployment"
    endpoint = "https://test-endpoint.com"
    # api_key = "test_api_key"
    api_version = "2023-03-15-preview"
    logger = Logger("test_logger")

    with pytest.raises(
        ValueError, match="The Azure API key cannot be `None` or empty`"
    ):
        AzureTextCompletion(
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key="",
            api_version=api_version,
            logger=logger,
        )


def test_azure_text_completion_init_with_empty_endpoint() -> None:
    deployment_name = "test_deployment"
    # endpoint = "https://test-endpoint.com"
    api_key = "test_api_key"
    api_version = "2023-03-15-preview"
    logger = Logger("test_logger")

    with pytest.raises(
        ValueError, match="The Azure endpoint cannot be `None` or empty"
    ):
        AzureTextCompletion(
            deployment_name=deployment_name,
            endpoint="",
            api_key=api_key,
            api_version=api_version,
            logger=logger,
        )


def test_azure_text_completion_init_with_invalid_endpoint() -> None:
    deployment_name = "test_deployment"
    endpoint = "http://test-endpoint.com"
    api_key = "test_api_key"
    api_version = "2023-03-15-preview"
    logger = Logger("test_logger")

    with pytest.raises(ValueError, match="The Azure endpoint must start with https://"):
        AzureTextCompletion(
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
            logger=logger,
        )


@pytest.mark.asyncio
async def test_azure_text_completion_call_with_parameters() -> None:
    mock_openai = AsyncMock()
    with patch(
        "semantic_kernel.connectors.ai.open_ai.services.open_ai_text_completion.openai",
        new=mock_openai,
    ):
        deployment_name = "test_deployment"
        endpoint = "https://test-endpoint.com"
        api_key = "test_api_key"
        api_type = "azure"
        api_version = "2023-03-15-preview"
        logger = Logger("test_logger")
        prompt = "hello world"
        complete_request_settings = CompleteRequestSettings()
        azure_text_completion = AzureTextCompletion(
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
            logger=logger,
        )

        await azure_text_completion.complete_async(prompt, complete_request_settings)

        mock_openai.Completion.acreate.assert_called_once_with(
            engine=deployment_name,
            api_key=api_key,
            api_type=api_type,
            api_base=endpoint,
            api_version=api_version,
            organization=None,
            prompt=prompt,
            temperature=complete_request_settings.temperature,
            max_tokens=complete_request_settings.max_tokens,
            top_p=complete_request_settings.top_p,
            presence_penalty=complete_request_settings.presence_penalty,
            frequency_penalty=complete_request_settings.frequency_penalty,
            stop=None,
            n=complete_request_settings.number_of_responses,
            stream=False,
            logit_bias=None,
        )


@pytest.mark.asyncio
async def test_azure_text_completion_call_with_parameters_logit_bias_not_none() -> None:
    mock_openai = AsyncMock()
    with patch(
        "semantic_kernel.connectors.ai.open_ai.services.open_ai_text_completion.openai",
        new=mock_openai,
    ):
        deployment_name = "test_deployment"
        endpoint = "https://test-endpoint.com"
        api_key = "test_api_key"
        api_type = "azure"
        api_version = "2023-03-15-preview"
        logger = Logger("test_logger")
        prompt = "hello world"
        complete_request_settings = CompleteRequestSettings()

        token_bias = {200: 100}
        complete_request_settings.token_selection_biases = token_bias

        azure_text_completion = AzureTextCompletion(
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
            logger=logger,
        )

        await azure_text_completion.complete_async(prompt, complete_request_settings)

        mock_openai.Completion.acreate.assert_called_once_with(
            engine=deployment_name,
            api_key=api_key,
            api_type=api_type,
            api_base=endpoint,
            api_version=api_version,
            organization=None,
            prompt=prompt,
            temperature=complete_request_settings.temperature,
            max_tokens=complete_request_settings.max_tokens,
            top_p=complete_request_settings.top_p,
            presence_penalty=complete_request_settings.presence_penalty,
            frequency_penalty=complete_request_settings.frequency_penalty,
            stop=None,
            n=complete_request_settings.number_of_responses,
            stream=False,
            logit_bias=token_bias,
        )
