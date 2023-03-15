﻿// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;
using System.Net.Http;
using System.Text.Json.Serialization;
using Microsoft.SemanticKernel.Skills.Memory.Qdrant.SDKClient.Internal.Diagnostics;

namespace Microsoft.SemanticKernel.Skills.Memory.Qdrant.SDKClient.Internal.Http.Specs;

internal class DeleteVectorsRequest : IValidatable
{
    [JsonPropertyName("points")]
    public List<string> Ids { get; set; }

    public static DeleteVectorsRequest DeleteFrom(string collectionName)
    {
        return new DeleteVectorsRequest(collectionName);
    }

    public void Validate()
    {
        Verify.NotNullOrEmpty(this._collectionName, "The collection name is empty");
        Verify.NotNullOrEmpty(this.Ids, "The list of vectors to delete is NULL or empty");
    }

    public DeleteVectorsRequest DeleteVector(string qdrantPointId)
    {
        Verify.NotNullOrEmpty(qdrantPointId, "The point ID is empty");
        this.Ids.Add(qdrantPointId);
        return this;
    }

    public HttpRequestMessage Build()
    {
        this.Validate();
        return HttpRequest.CreatePostRequest(
            $"collections/{this._collectionName}/points/delete",
            payload: this);
    }

    #region private ================================================================================

    private readonly string _collectionName;

    private DeleteVectorsRequest(string collectionName)
    {
        this.Ids = new List<string>();
        this._collectionName = collectionName;
    }

    #endregion
}
