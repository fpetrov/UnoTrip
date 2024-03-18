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
    public string Name { get; set; }
    public DateTime Start { get; set; }
    public DateTime End { get; set; }
}

public class Note
{
    [Key]
    public int Id { get; set; }
    public User Author { get; set; }
    public string Text { get; set; }
    public bool IsPrivate { get; set; }
}

/// <summary>
/// Файлы и различные картинки для путешествия.
/// </summary>
public class File
{
    public string Name { get; set; }
    public string Path { get; set; }
}