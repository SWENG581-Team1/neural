#gin_table.seat_player test strategy
##Control Flow
[Control Flow](gin_table.seat_player.control_flow.png)

|   Scenario   |Node   |   Node Description    |   Interpretation   |
|:--------:|:----:|----------------|--------------|
|1|1|seat_player(self, player)| |
| |2(F)|self.player1 is not False and self.player1.id == player.id) or (self.player2 is not False and self.player2.id == player.id) | self.player1 == player |
| |3| raise TableSeatingError |  |
|2|1|seat_player(self, player)| |
| |2(T)|self.player1 is not False and self.player1.id == player.id) or (self.player2 is not False and self.player2.id == player.id) | player1 == null and player2 == null |
| |4(T)| not self.player1 | self.player1 == null |
| |5| self.player1 = player self.player1.table = self return True | table.player1 == player |
|3|1|seat_player(self, player)| |
| |2(T)|self.player1 is not False and self.player1.id == player.id) or (self.player2 is not False and self.player2.id == player.id) | player1 == null and player2 == null |
| |4(F)|not self.player1 | player1 != null |
| | 6(T) | not self.player2 | player2 == null |
| | 7 | self.player2 = player self.player2.table = self return True | player2 == player |
| 4 | 1|seat_player(self, player)| |
| |2(T)|self.player1 is not False and self.player1.id == player.id) or (self.player2 is not False and self.player2.id == player.id) | player1 == null and player2 == null |
| |4(F)|not self.player1 | player1 != null |
| | 6(F) | not self.player2 | player2 != null |
| | 8 | raise TableSeatingError("gintable is full") |--|

 
