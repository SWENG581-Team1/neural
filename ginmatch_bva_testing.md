# The ginmatch.process_knock_gin BVA testing.
The process_knock_gin and process_knock methods is are good targets for BVA testing because it's inputs can be easily and clearly divided into three categories.  Each of these categories applies to both methods the same results.

1. Gin (Zero deadwood)
2. Valid knock, not gin (1-10 points of deadwood)
3. Invalid nock (11 or more points of deadwood)

Effectively testing the boarder values requires testing at, below and above the borders.
1. 0 points of deadwood (Gin, on border)
2. 1 point of deadwood. (Valid knock, not gin, above border)
3. 10 points of deadwood. (Valid knock, not gin, on border)
4. 11 points of deadwood. (Invalid knock, above border)

## Input hands
1. Gin [1H, 2H, 3H, 4H, 5H, 6H, 7H, 8H, 9H, 10H]
2. 1 point of deadwood [1D, 2H, 3H, 4H, 5H, 6H, 7H, 8H, 9H, 10H]
3. 10 points of deadwood [1H, 2H, 3H, 4H, 5H, 6H, 7H, 8H, 9H, 10D]
4. 11 points of deadwood [1D, 2H, 3H, 4H, 5H, 6H, 7H, 8H, 9H, 10D]

Unfortunately these methods do not have a return value, so we must observe the state changes in other attributes.  These attributes include:

1. knocked_improperly
2. game_over
3. player_who_knocked
4. player_who_knocked_gin

## Expected output process_knock and process_knock_gin
| Input                | knocked_improperly | game_over | player_who_knocked | player_who_knocked_gin |
|----------------------|--------------------|-----------|--------------------|------------------------|
| Gin                  | False              | True      | False              | True                   |
| Valid knock, not gin | False              | True      | True               | False                  |
| Not Gin              |  True              | False     | False              | False                  |

## Actions taken
The existing test architecture provided test cases that tested an aweful hand (55 points of deadwood), a valid knock (10 points of deadwood), and gin (0 points of deadwood).  In order to establish BVA testing, test cases were added for 1 point and 11 points of deadwood.
