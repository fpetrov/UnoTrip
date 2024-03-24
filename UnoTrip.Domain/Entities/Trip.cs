using System.ComponentModel.DataAnnotations;

namespace UnoTrip.Domain.Entities;

public class Trip
{
    [Key]
    public int Id { get; set; }
    public Guid Uuid { get; set; }
    public string Name { get; set; }
    public string Description { get; set; }
    public List<Note> Notes { get; set; } = [];
    public List<User> Subscribers { get; set; } = [];
    public List<Location> Locations { get; set; } = [];
}

public class Location
{
    [Key]
    public int Id { get; set; }
    public string Name { get; set; }
    public float Latitude { get; set; }
    public float Longitude { get; set; }
    public DateOnly Start { get; set; }
    public DateOnly End { get; set; }
}

/// <summary>
/// Заметка в путешествии. Представляет собой id файла в Telegram
/// </summary>
public class Note
{
    [Key]
    public int Id { get; set; }
    public string Name { get; set; }
    public string ContentType { get; set; }
    public User Author { get; set; }
    public string FileId { get; set; }
    public bool IsPrivate { get; set; }
}