using System.ComponentModel.DataAnnotations;

namespace UnoTrip.Domain.Entities;

public class User
{
    [Key]
    public int Id { get; set; }
    public string Description { get; set; }
    public string City { get; set; }
    public string Country { get; set; }
    public int Age { get; set; }
}