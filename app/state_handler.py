from match_handler import *
import copy 

PARCIAL_MATCHES: List[MatchOut] = []

def add_parcial_match(match_: MatchOut):
    match_out = copy.deepcopy(match_)
    matches_by_id: List[MatchOut] = [match for match in PARCIAL_MATCHES if match.match_id == match_out.match_id]

    if matches_by_id:
        new_state = max(match.state for match in matches_by_id) + 1
        if new_state != 4:
            match_out.state = new_state
            PARCIAL_MATCHES.append(match_out)
    else:
        match_out.state = 0
        PARCIAL_MATCHES.append(match_out)

    
def get_parcial_match(match_id: UUID) -> MatchOut:
    matches_by_id: List[MatchOut] = [match for match in PARCIAL_MATCHES if match.match_id == match_id]
    
    if matches_by_id:
        max_state = max(match.state for match in matches_by_id)
        last_parcial_match = next(match for match in matches_by_id if match.state == max_state)
        return last_parcial_match
    else:
        return None
    
def remove_last_parcial_match(match_id: UUID) -> bool:
    matches_by_id: List[MatchOut] = [match for match in PARCIAL_MATCHES if match.match_id == match_id]

    if matches_by_id:
        max_state = max(match.state for match in matches_by_id)
        
        last_parcial_match = next(match for match in matches_by_id if match.state == max_state)
        PARCIAL_MATCHES.remove(last_parcial_match)
        
        return True
    else:
        return False

