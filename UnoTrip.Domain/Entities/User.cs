using System.ComponentModel.DataAnnotations;

namespace UnoTrip.Domain.Entities;

public class User
{
    [Key]
    public int Id { get; set; }
    public long TelegramId { get; set; }
    public string Description { get; set; }
    public string City { get; set; }
    public int Age { get; set; }

    public List<Trip> Trips { get; set; } = [];
}