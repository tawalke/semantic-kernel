﻿// Copyright (c) Microsoft. All rights reserved.

namespace Microsoft.SemanticKernel.Skills.Memory.Qdrant.SDKClient.Internal.Diagnostics;

public class VectorDbException : Exception<VectorDbException.ErrorCodes>
{
    public enum ErrorCodes
    {
        UnknownError,
        CollectionDoesNotExist,
        InvalidCollectionState,
    }

    public VectorDbException(string message)
        : this(ErrorCodes.UnknownError, message)
    {
    }

    public VectorDbException(ErrorCodes error, string message)
        : base(error, message)
    {
    }

    public VectorDbException()
    {
    }
}
