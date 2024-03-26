using Riok.Mapperly.Abstractions;
using UnoTrip.Application.Trip.Common;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Application.Common.Mappings;

[Mapper]
public static partial class NoteMapper
{
    public static partial NoteResult Map(Note note);
}