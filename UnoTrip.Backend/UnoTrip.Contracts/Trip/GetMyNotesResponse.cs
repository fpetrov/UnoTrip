namespace UnoTrip.Contracts.Trip;

public record GetMyNotesResponse(
    List<NoteResponse> Notes);