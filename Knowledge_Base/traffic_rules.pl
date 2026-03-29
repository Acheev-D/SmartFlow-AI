% --- SmartFlow Prolog Knowledge Base ---
% Purpose: Neuro-Symbolic Reasoning Layer for Adaptive Traffic Control.
% This file defines the formal logic rules that govern signal transitions.

% --- 1. DYNAMIC DATA DECLARATIONS ---
% These predicates allow the Python 'Vision Engine' to assert facts into the brain.
:- dynamic status/2.      % status(LaneID, Condition) -> e.g., status(lane_n, emergency)
:- dynamic pressure/2.    % pressure(LaneID, Value)     -> e.g., pressure(lane_s, 18.5)
:- dynamic wait_time/2.   % wait_time(LaneID, Seconds)  -> e.g., wait_time(lane_e, 72)
:- dynamic junction/1.    % junction(Condition)         -> e.g., junction(pedestrians_present)

% --- 2. THE EXPERT RULESET ---

% [RULE: EMERGENCY PRIORITY]
% The signal MUST switch if an emergency vehicle is detected, regardless of density.
should_switch(Lane) :- 
    status(Lane, emergency).

% [RULE: CONGESTION MANAGEMENT]
% Switch if the lane pressure exceeds the threshold and the cross-traffic is lower.
should_switch(Lane) :- 
    pressure(Lane, P), P > 15,
    cross_lane(Lane, Other),
    pressure(Other, OP), OP < (P * 0.5).

% [RULE: STARVATION PREVENTION]
% Even if density is low, switch if drivers have been waiting too long.
should_switch(Lane) :- 
    wait_time(Lane, T), T > 60.

% [RULE: SAFETY OVERRIDE]
% A switch to green is ONLY authorized if the junction is clear of pedestrians.
is_safe_to_switch :- 
    \+ junction(pedestrians_present).

% --- 3. INFRASTRUCTURE FACTS ---
cross_lane(lane_n, lane_e).
cross_lane(lane_s, lane_w).
cross_lane(lane_e, lane_n).
cross_lane(lane_w, lane_s).

% --- 4. CLI EXECUTION HARNESS (For Command Line Evaluation) ---
% This predicate allows an evaluator to run the logic without a GUI.
% Usage: swipl -q -s traffic_rules.pl -g "run_logic_test(lane_n, emergency, 20, 5, 10)." -t halt

run_logic_test(TargetLane, CurrentStatus, LanePressure, OtherPressure, WaitT) :-
    % Initialize Mock Facts
    retractall(status(_,_)),
    retractall(pressure(_,_)),
    retractall(wait_time(_,_)),
    retractall(junction(_)),
    
    assertz(status(TargetLane, CurrentStatus)),
    assertz(pressure(TargetLane, LanePressure)),
    assertz(pressure(lane_e, OtherPressure)), % Assuming East is the cross-lane
    assertz(wait_time(TargetLane, WaitT)),
    
    format('~n>>> SmartFlow AI: Symbolic Logic Audit~n'),
    format('Lane: ~w | Status: ~w | Pressure: ~w | Wait: ~w s~n', 
           [TargetLane, CurrentStatus, LanePressure, WaitT]),
    
    % Execute Reasoning
    (is_safe_to_switch ->
        (should_switch(TargetLane) -> 
            format('DECISION: [SWITCH_SIGNAL] -> Priority heuristics satisfied.~n')
        ;   format('DECISION: [HOLD_SIGNAL] -> Current flow is efficient.~n')
        )
    ;   format('DECISION: [SAFETY_HALT] -> Junction blocked by pedestrians.~n')
    ).