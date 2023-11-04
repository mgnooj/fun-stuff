# How Did Contra Detect the Konami Code (on the NES)?

On a game console where every bit had to be squeezed for performance, how much of the system resources did Konami developers allocate to accomplishing the crucial task of scanning user input for the Konami Code?

Thankfully, GitHub user vermiceli recently shared a [complete and commented dissassembly of the NES version of Contra](https://github.com/vermiceli/nes-contra-us/), so we can check out the original algorithm:

    ; checks if current input is part of Kazuhisa Hashimoto's famous Konami code (30-lives code)
    ; if completed input successfully, set KONAMI_CODE_STATUS to #$01
    konami_input_check:
        ldy KONAMI_CODE_NUM_CORRECT    ; load the number of successful inputs of Konami code
        bmi konami_code_exit           ; if #$ff (invalid Konami input), exit
        lda CONTROLLER_STATE_DIFF      ; buttons pressed (only care on input change so held button doesn't affect code)
        and #$cf                       ; only care about input from d-pad and A/B buttons (not select nor start)
        beq konami_code_exit           ; if no input detected, exit
        cmp konami_code_lookup_table,y ; compare with Konami code sequence at index y
        beq konami_input_index_correct ; on success, goto konami_input_index_correct
        lda #$ff                       ; incorrect sequence for Konami code
        sta KONAMI_CODE_NUM_CORRECT    ; since incorrect set KONAMI_CODE_NUM_CORRECT (number of successful inputs) to $ff
        rts

    konami_input_index_correct:
        iny                         ; add to number of successfully entered Konami code inputs
        sty KONAMI_CODE_NUM_CORRECT ; store in KONAMI_CODE_NUM_CORRECT
        cpy #$0a                    ; Konami code is 10 inputs, compare against how many successfully entered
        bcc konami_code_exit        ; Konami code not yet fully entered, exit
        lda #$01                    ; Konami code successfully entered, set flag to $01
        sta KONAMI_CODE_STATUS      ; store success flag in memory

    konami_code_exit:
        rts

    ; table for Konami code (30-lives code) - up up down down ...
    konami_code_lookup_table:
        .byte $08,$08,$04,$04,$02,$01,$02,$01,$40,$80

Source: [https://github.com/vermiceli/nes-contra-us/blob/main/src/bank7.asm](https://github.com/vermiceli/nes-contra-us/blob/main/src/bank7.asm)

Let's break this down:

- KONAMI_CODE_NUM_CORRECT stores a running count of the number of consecutive Konami code button presses. (By extension, every time you press "UP", this value gets incremented; and so on for each additional correct button input.)
- KONAMI_CODE_STATUS reserves a bit as a 'success' switch for when the full code has been detected.
- konami_code_lookup_table is a byte array representation of the Konami code.
- konami_input_check gets any current user input and compares it to the element of the lookup table at index KONAMI_CODE_NUM_CORRECT.
If they are identical, konami_input_index_correct is called; else, KONAMI_CODE_NUM_CORRECT is reset to zero.
- konami_input_index_correct increments KONAMI_CODE_NUM_CORRECT and then checks if it is equal to 10. If it is, the KONAMI_CODE_STATUS flag is raised; else, we exit the process.

In other words, the user input is never stored; instead, the algorithm counts consecutive Konami code button presses by comparing the current input to a Konami code lookup table at a given index (i.e. the current count of correct Konami code button presses).

During the game loop initialization, KONAMI_CODE_STATUS is read:

    init_player_lives:
        lda #$02                  ; start of with #$02 lives
        ldy KONAMI_CODE_STATUS    ; 30-lives code switch ($01 = code activated)
        beq init_player_num_lives ; if KONAMI_CODE_STATUS is not set, then just set 2 lives
        lda #$1d                  ; KONAMI_CODE_STATUS active so set lives to #$1d (29 decimal)

If the 'success' switch is active, P1_NUM_LIVES is set to 29; else it is set to the default 2.

That's it! Those were simpler times.

All credit to [vermiceli](https://github.com/vermiceli/nes-contra-us/) for the code.
