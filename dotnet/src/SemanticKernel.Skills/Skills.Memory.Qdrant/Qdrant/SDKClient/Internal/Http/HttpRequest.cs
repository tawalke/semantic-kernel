﻿// Copyright (c) Microsoft. All rights reserved.

using System.Net.Http;
using System.Net.Mime;
using System.Text;
using System.Text.Json;

namespace Microsoft.SemanticKernel.Skills.Memory.Qdrant.SDKClient.Internal.Http;

internal static class HttpRequest
{
    public static HttpRequestMessage CreateGetRequest(string url)
    {
        return new HttpRequestMessage(HttpMethod.Get, url);
    }

    public static HttpRequestMessage CreatePostRequest(string url, object? payload = null)
    {
        return new HttpRequestMessage(HttpMethod.Post, url)
        {
            Content = GetJsonContent(payload)
        };
    }

    public static HttpRequestMessage CreatePutRequest(string url, object? payload = null)
    {
        return new HttpRequestMessage(HttpMethod.Put, url)
        {
            Content = GetJsonContent(payload)
        };
    }

    public static HttpRequestMessage CreatePatchRequest(string url, object? payload = null)
    {
        return new HttpRequestMessage(HttpMethod.Patch, url)
        {
            Content = GetJsonContent(payload)
        };
    }

    public static HttpRequestMessage CreateDeleteRequest(string url)
    {
        return new HttpRequestMessage(HttpMethod.Delete, url);
    }

    public static StringContent? GetJsonContent(object? payload)
    {
        if (payload != null)
        {
            if (payload is string strPayload)
            {
                return new StringContent(strPayload);
            }

            var json = JsonSerializer.Serialize(payload);
            return new StringContent(json, Encoding.UTF8, MediaTypeNames.Application.Json);
        }

        return null;
    }
}
