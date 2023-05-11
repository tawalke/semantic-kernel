﻿// Copyright (c) Microsoft. All rights reserved.

using System.Text.Json.Serialization;
using SemanticKernel.Service.Storage;

namespace SemanticKernel.Service.Model;

/// <summary>
/// A chat session
/// </summary>
public class ChatSession : IStorageEntity
{
    /// <summary>
    /// Chat ID that is persistent and unique.
    /// </summary>
    [JsonPropertyName("id")]
    public string Id { get; set; }

    /// <summary>
    /// User ID that is persistent and unique.
    /// </summary>
    [JsonPropertyName("userId")]
    public string UserId { get; set; }

    /// <summary>
    /// Title of the chat.
    /// </summary>
    [JsonPropertyName("title")]
    public string Title { get; set; }

    /// <summary>
    /// Timestamp of the message.
    /// </summary>
    [JsonPropertyName("timestamp")]
    public DateTimeOffset Timestamp { get; set; }

    public ChatSession(string userId, string title)
    {
        this.Id = Guid.NewGuid().ToString();
        this.UserId = userId;
        this.Title = title;
        this.Timestamp = DateTimeOffset.Now;
    }
}
