;;; General information:
;;; ;;;;;;;;;;;;;;;;;;;;
;;; r31 is the return address (ra)
;;; r30 is the stack pointer (sp)
;;; r25 to r29 are temporary and always overridable
;;; r20 to r24 are used for passing arguments and should be saved if overridden
;;; ;;;;;;;;;;;;;;;;;;;;
;;; bignums are represented in base 256
;;; for the endianness coherency, most significant digits are at smaller indices
;;; e.g. if the number 0x12ab34cd is stored at address 100 :
;;;   value: 12 ab 34 cd   4
;;; address: 96 97 98 99 100

push_tmp_registers_1:
  sub r30 r30 #1                ; decr sp
  mov !r30,#0 r25               ; push r25
  ret

pop_tmp_registers_1:
  mov r25 !r30,#0               ; pop r25
  add r30 r30 #1                ; incr sp
  ret

push_tmp_registers_2:
  sub r30 r30 #2                ; decr sp
  mov !r30,#0 r25               ; push r25
  mov !r30,#1 r26               ; push r26
  ret

pop_tmp_registers_2:
  mov r26 !r30,#1               ; pop r26
  mov r25 !r30,#0               ; pop r25
  add r30 r30 #2                ; incr sp
  ret

push_tmp_registers_3:
  sub r30 r30 #3                ; decr sp
  mov !r30,#0 r25               ; push r25
  mov !r30,#1 r26               ; push r26
  mov !r30,#2 r27               ; push r27
  ret

pop_tmp_registers_3:
  mov r27 !r30,#2               ; pop r27
  mov r26 !r30,#1               ; pop r26
  mov r25 !r30,#0               ; pop r25
  add r30 r30 #3                ; incr sp
  ret

push_tmp_registers_4:
  sub r30 r30 #4                ; decr sp
  mov !r30,#0 r25               ; push r25
  mov !r30,#1 r26               ; push r26
  mov !r30,#2 r27               ; push r27
  mov !r30,#3 r28               ; push r28
  ret

pop_tmp_registers_4:
  mov r28 !r30,#3               ; pop r28
  mov r27 !r30,#2               ; pop r27
  mov r26 !r30,#1               ; pop r26
  mov r25 !r30,#0               ; pop r25
  add r30 r30 #4                ; incr sp
  ret

push_tmp_registers_5:
  sub r30 r30 #5                ; decr sp
  mov !r30,#0 r25               ; push r25
  mov !r30,#1 r26               ; push r26
  mov !r30,#2 r27               ; push r27
  mov !r30,#3 r28               ; push r28
  mov !r30,#4 r29               ; push r29
  ret

pop_tmp_registers_5:
  mov r29 !r30,#4               ; pop r29
  mov r28 !r30,#3               ; pop r28
  mov r27 !r30,#2               ; pop r27
  mov r26 !r30,#1               ; pop r26
  mov r25 !r30,#0               ; pop r25
  add r30 r30 #5                ; incr sp
  ret

print_newline:
  prc #10                       ; 10 is \n
 	ret

bignum_print:
  ;; print r20
  sub r25 r20 !r20              ; most significant byte address
_bn_print__loop:
  prx !r25                      ; print digit
  add r25 r25 #1                ; incr address
  bne _bn_print__loop r25 r20   ; loop until final byte
  sub r30 r30 #1                ; decr sp
  mov !r30 r31                  ; push ra
  cal print_newline
  mov r31 !r30                  ; pop ra
  add r30 r30 #1                ; incr sp
  ret

bignum_init:
  ;; initialize a number of size r21 at address r20
  mov !r20 r21                  ; number size
  sub r25 r20 r21               ; most significant byte address
_bn_init__loop:
  mov !r25 #0                   ; init byte
  add r25 r25 #1                ; incr address
  bne _bn_init__loop r25 r20    ; loop until least significant byte
  ret

bignum_cleanup:
  sub r25 r20 !r20
_bn_cleanup__loop:
  bne _bn_cleanup__end !r25 #0
  beq _bn_cleanup__zero r25 r20
  add r25 r25 #1
  sub !r20 !r20 #1
  jmp _bn_cleanup__loop
_bn_cleanup__zero:
  mov !r20 #1
_bn_cleanup__end:
  ret

bignum_zero:
  ;; set length to 0 if bignum = 0
  ;; a bignum is zero if its lsB is 0 and its length is 1
  cmp r25 !r20 #1               ; compare length to 1
  bne _bn_zero_no r25 #0        ; if not it is not 0
  bne _bn_zero_no !r20,#-1 #0   ; idem if lsb is not 0
  mov !r20 #0
_bn_zero_no:
  ret

bignum_clear:
  ;; reset r20
  sub r25 r20 !r20              ; most significant byte address
_bn_clear__loop:
  mov !r25 #0                   ; reset byte
  add r25 r25 #1                ; incr address
  bne _bn_clear__loop r25 r20   ; loop until least significant byte
  ret

bignum_copy:
  ;; r20 = r21
  beq _bn_copy__cp !r20 #0
  sub r30 r30 #1                ; decr sp
  mov !r30 r31                  ; push ra
  cal bignum_clear
  mov r31 !r30                  ; pop ra
  add r30 r30 #1                ; incr sp
_bn_copy__cp:
  mov !r20 !r21
  sub r25 #0 !r20
  beq _bn_copy__end r25 #0
_bn_copy__loop:
  mov !r20,r25 !r21,r25
  add r25 r25 #1
  bne _bn_copy__loop r25 #0
_bn_copy__end:
  ret

bignum_cmp:
  ;; cmp r20 r21 r24
  beq _bn_cmp_same r21 r24
  cmp r20 !r21 !r24
  bne _bn_cmp_done r20 #0
  sub r25 #0 !r21              ; r25 = -len
_bn_cmp_loop:
  beq _bn_cmp_same r25 #0
  cmp r20 !r21,r25 !r24,r25
  bne _bn_cmp_done r20 #0
  add r25 r25 #1
  jmp _bn_cmp_loop
_bn_cmp_same:
  mov r20 #0
_bn_cmp_done:
  ret

bignum_sub:
  ;; r20 = r20 - r24 (with r20 >= r24)
  mov r25 #0
  mov r26 #0                    ; borrow
_bn_sub_loop:
  sub r25 r25 #1
  sub !r20,r25 !r20,r25 !r24,r25
  sub !r20,r25 !r20,r25 r26
  cmp r27 !r20,r25 #0
  beq _bn_sub_neg r27 #1
  mov r26 #0
  jmp _bn_sub_endloop
_bn_sub_neg:
  add !r20,r25 !r20,r25 #256
  mov r26 #1
_bn_sub_endloop:
  add r27 r25 !r24
  beq _bn_sub_end r27 #0
  jmp _bn_sub_loop
_bn_sub_end:
  sub r25 r25 #1
  sub !r20,r25 !r20,r25 r26
  sub r30 r30 #1                ; decr sp
  mov !r30 r31                  ; push ra
  cal bignum_cleanup
  mov r31 !r30                  ; pop ra
  add r30 r30 #1                ; incr sp
  ret

bignum_add:
  ;; r20 = r21 + r22 mod r24
  ;; init r20
  sub r30 r30 #2                ; decr sp
  mov !r30,#1 r21               ; push r21
  mov !r30 r31                  ; push ra
  cmp r25 !r21 !r22
  beq _bn_add__lt r25 #1
  add r21 !r21 #1
  jmp _bn_add__init
_bn_add__lt:
  add r21 !r22 #1
_bn_add__init:
  cal bignum_init
  mov r31 !r30                  ; pop ra
  mov r21 !r30,#1               ; pop r21
  add r30 r30 #2                ; incr sp
_bn_add__add:
  sub r28 #0 !r20               ; number size
  mov r25 #0                    ; counter
  mov r26 #0                    ; carry
_bn_add__loop:
  sub r25 r25 #1                ; decr counter
  add r27 !r21,r25 !r22,r25     ; tmp add byte
  add r27 r27 r26               ; tmp add carry
  mod !r20,r25 r27 #256         ; new byte
  div r26 r27 #256              ; new carry
  bne _bn_add__loop r25 r28     ; continue as long as bytes exist
  ;; modulus
  sub r30 r30 #1                ; decr sp
  mov !r30 r31                  ; push ra
  mov r25 r20
  mov r21 r20
  cal push_tmp_registers_1
  cal bignum_cleanup
  cal pop_tmp_registers_1
  cal push_tmp_registers_3
  cal bignum_cmp
  cal pop_tmp_registers_3
  beq _bn_add_end r20 #1
  mov r20 r25
  cal push_tmp_registers_3
  cal bignum_sub
  cal pop_tmp_registers_3
_bn_add_end:
  mov r31 !r30                  ; pop ra
  add r30 r30 #1                ; incr sp
  mov r20 r25
  ret

bignum_rshift:
  ;; r20 = r20 >> r21
  div r26 r21 #8                ; number of complete bytes to shift (n)
  sub r25 r20 #1
  sub r25 r25 r26               ; address of future least significant byte (flsB)
  sub r27 r20 !r20              ; address of most significant byte (msB)
  cmp r28 r27 r25               ; continue only if flsB > msB (r28 is 1)
  beq _bn_rshift__zero r28 #-1  ; if flsB < msB we're done
_bn_rshift__bytes:
  beq _bn_rshift__bits r28 #0   ; else if flsB = msB go shift bits
  mov !r25,r26 !r25             ; else shift flsB of n bytes
  cmp r28 r25 r27               ; continue only if flsB > msB (r28 is 1)
  sub r25 r25 #1                ; decr address
  jmp _bn_rshift__bytes
_bn_rshift__bits:
  add r26 r27 r26               ; msB after shift of bytes
  mod r25 r21 #8                ; number of bits to shift (n)
  beq _bn_rshift__clean r25 #0  ; n = 0
_bn_rshift__b:
  mov r29 r20
_bn_rshift__B:
  sub r29 r29 #1                ; current byte (B)
  lsr !r29 !r29 #1              ; B >> 1
  and r28 !r29,#-1 #1           ; lsb of previous byte (b)
  lsl r28 r28 #7                ; b << 7
  orr !r29 !r29 r28             ; B = B | b
  bne _bn_rshift__B r29 r26
  sub r25 r25 #1
  bne _bn_rshift__b r25 #0
  jmp _bn_rshift__clean
_bn_rshift__zero:               ; completely reset number
  sub r26 r20 #1                ; erase until lsB
_bn_rshift__clean:
  beq _bn_rshift__end r26 r27
  mov !r27 #0
  add r27 r27 #1
  jmp _bn_rshift__clean
_bn_rshift__end:
  sub r30 r30 #1                ; decr sp
  mov !r30 r31                  ; push ra
  cal bignum_cleanup
  mov r31 !r30                  ; pop ra
  add r30 r30 #1                ; incr sp
  ret

bignum_mul:
  ;; r20 = r21 * r22 mod r24
  ;; backup arguments and ra
  sub r30 r30 #4                ; decr sp
  mov !r30 r31                  ; push ra
  mov !r30,#1 r20               ; push r20 (r)
  mov !r30,#2 r21               ; push r21 (b)
  mov !r30,#3 r22               ; push r22 (e)

  ;; init r25 (res), r26 (base), r27 (exp), r28 (tmp)
  mov r25 r20                   ; r25 points on res (r20)
  mov r29 r21                   ; r29 backups b (r21)
  add r21 !r29 !r22             ; init len(res) to len(b) + len(e)
  cal push_tmp_registers_1
  cal bignum_init               ; res = 0
  cal pop_tmp_registers_1

  mov r26 #900000               ; base is stored at @900000
  mov r20 r26                   ; r20 is base
  mov r21 r29                   ; r21 is b
  cal push_tmp_registers_1
  cal bignum_copy               ; base = b
  cal pop_tmp_registers_1
_bn_mul_mod_base:
  mov r21 r26
  ;; mov r20 r26
  ;; cal bignum_print
  cal push_tmp_registers_3
  cal bignum_cmp
  cal pop_tmp_registers_3
  beq _bn_mul_mod_base_end r20 #1
  mov r20 r26
  cal push_tmp_registers_3
  cal bignum_sub
  cal pop_tmp_registers_3
  jmp _bn_mul_mod_base
_bn_mul_mod_base_end:

  mov r27 #910000               ; exp is stored at @910000
  mov r20 r27                   ; r20 is exp
  mov r21 r22                   ; r21 is e (r22)
  cal push_tmp_registers_1
  cal bignum_copy               ; exp = e
  cal pop_tmp_registers_1

  mov r28 #920000               ; tmp is stored at @920000
  mov r20 r28                   ; r20 is tmp
  add r21 !r26 !r27             ; init len(tmp) to len(base) + len(exp)
  cal push_tmp_registers_1
  cal bignum_init               ; tmp = 0
  cal pop_tmp_registers_1

_bn_mul__loop:
  mov r20 r27
  cal push_tmp_registers_1
  cal bignum_zero
  cal pop_tmp_registers_1
  beq _bn_mul__end !r27 #0      ; if exp = 0: multiplication finished
  and r29 !r27,#-1 #1           ; otherwise: r28 = lsb of exp
  bne _bn_mul__double r29 #1
_bn_mul__add:
  mov r20 r28                   ; r20 is tmp
  mov r21 r25                   ; r21 is res
  cal push_tmp_registers_1
  cal bignum_copy               ; tmp = res
  cal pop_tmp_registers_1
  mov r20 r25                   ; r20 is res
  mov r21 r28                   ; r21 is tmp
  mov r22 r26                   ; r22 is base
  cal push_tmp_registers_4
  cal bignum_add                ; res = tmp + base
  cal pop_tmp_registers_4
_bn_mul__double:
  mov r20 r28                   ; r20 is tmp
  mov r21 r26                   ; r21 is base
  cal push_tmp_registers_1
  cal bignum_copy               ; tmp = base
  cal pop_tmp_registers_1
  mov r20 r26                   ; r20 is base
  mov r21 r28                   ; r21 is tmp
  mov r22 r28                   ; r22 is tmp
  cal push_tmp_registers_4
  cal bignum_add                ; base = tmp + tmp
  cal pop_tmp_registers_4
_bn_mul__shift:
  mov r20 r27                    ; r20 is exp
  mov r21 #1                     ; r21 is 1
  cal push_tmp_registers_5
  cal bignum_rshift              ; exp = exp >> 1
  cal pop_tmp_registers_5
  jmp _bn_mul__loop
_bn_mul__end:
  ;; restore arguments and ra
  mov r22 !r30,#3               ; pop r22
  mov r20 !r30,#2               ; pop r21
  mov r20 !r30,#1               ; pop r20
  mov r31 !r30                  ; pop ra
  add r30 r30 #4                ; incr sp
  ret
