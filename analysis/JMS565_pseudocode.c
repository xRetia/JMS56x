/*
 * JMS565 firmware 105.03.01.02 -- reconstructed C-style pseudocode
 * Source image SHA-256: c65feffa30f9697ae383ecbd4b90514c53f1f8ec8ed2de380abddfff2718d623
 *
 * IMPORTANT:
 * - This is analysis pseudocode, NOT original vendor source and not buildable firmware.
 * - 8051 direct-bit addresses E7 below denote ACC.7 after MOVX A,@DPTR.
 * - Several call/jump targets land in zero-filled image holes. Those are left as
 *   unresolved ROM/bank/overlay calls; the dump alone does not reveal semantics.
 * - Addresses are CPU CODE/XDATA addresses as used in the listing; the chip's
 *   banked mapping and register names are not available in this dump.
 */
#include <stdint.h>

extern uint8_t xdata_read8(uint16_t addr);
extern void    xdata_write8(uint16_t addr, uint8_t value);
extern void    iram_write8(uint8_t addr, uint8_t value);
extern uint8_t bit_read(uint8_t bit_address);
extern void    call_unresolved(uint16_t code_address);
extern void    jump_unresolved(uint16_t code_address);
extern volatile uint8_t callback_low_54;
extern volatile uint8_t callback_high_55;

/* Reset vector at CPU CODE 0000. Verified bytes: 02 80 16 (LJMP 8016). */
void reset_vector_0000(void)
{
    jump_unresolved(0x8016);
}

/*
 * Actual reset target at CPU CODE 8016. Verified instruction sequence:
 *   LCALL DAFD;
 *   XDATA[5048..504B] = 20 00 00 00;
 *   if RAM bit 00 is set, LCALL DDE0;
 *   otherwise LCALL DDEA and XDATA[0052]=XDATA[0062]=3C;
 *   clear bit7 of XDATA[7019]; LCALL 74E5, 993D, BD0D;
 *   clear bit4 of XDATA[5064]; XDATA[5051]=80;
 *   set bit1 then clear bit0 of XDATA[5056]; LJMP DFBC.
 *
 * The helper/tail-jump targets DDE0, DDEA, BD0D and DFBC enter long zero
 * spans in the dump. Treat them as unresolved (ROM/bank/map or omitted content),
 * not as proven NOPs. XDATA register meanings are unknown.
 */
void reset_entry_8016(void)
{
    call_unresolved(0xDAFD);

    xdata_write8(0x5048, 0x20);
    xdata_write8(0x5049, 0x00);
    xdata_write8(0x504A, 0x00);
    xdata_write8(0x504B, 0x00);

    if (bit_read(0x00)) {
        call_unresolved(0xDDE0);
    } else {
        call_unresolved(0xDDEA);
        xdata_write8(0x0052, 0x3C);
        xdata_write8(0x0062, 0x3C);
    }

    xdata_write8(0x7019, xdata_read8(0x7019) & 0x7F);
    call_unresolved(0x74E5);
    call_unresolved(0x993D);
    call_unresolved(0xBD0D);
    xdata_write8(0x5064, xdata_read8(0x5064) & 0xEF);
    xdata_write8(0x5051, 0x80);
    xdata_write8(0x5056, xdata_read8(0x5056) | 0x02);
    xdata_write8(0x5056, xdata_read8(0x5056) & 0xFE);
    jump_unresolved(0xDFBC);
}

/*
 * Candidate USB/VBUS status callback at CODE C26F.
 * Object code directly proves:
 *   read XDATA[502E]; if ACC.7=1 call 9F59, set 54/55= A2BD, return;
 *   otherwise if XDATA[7E1B]==0 set XDATA[350C].bit1 and call D792;
 *   then set 54/55=9BDA and return.
 *
 * Function identity is inferred from neighboring ASCII strings
 * "vbus_debounce_1 !!!" and "vbus_debounce_0 !!!"; direct LCALL xrefs to C26F
 * were not found, so it may be indirectly dispatched, banked, or unused.
 */
void candidate_status_handler_C26F(void)
{
    uint8_t status = xdata_read8(0x502E);
    if (status & 0x80) {
        call_unresolved(0x9F59);     /* file target is in zero-filled span */
        callback_low_54  = 0xBD;
        callback_high_55 = 0xA2;    /* callback/address value A2BD */
        return;
    }

    if (xdata_read8(0x7E1B) == 0) {
        xdata_write8(0x350C, xdata_read8(0x350C) | 0x02);
        call_unresolved(0xD792);
    }
    callback_low_54  = 0xDA;
    callback_high_55 = 0x9B;        /* callback/address value 9BDA */
}

/* Parallel status path at CODE C297; same decision pattern, different port. */
void candidate_status_handler_C297(void)
{
    uint8_t status = xdata_read8(0x008B);
    if (status & 0x80) {
        call_unresolved(0x9F59);     /* file target is in zero-filled span */
        callback_low_54  = 0xBD;
        callback_high_55 = 0xD3;     /* callback/address value D3BD */
        return;
    }

    if (xdata_read8(0x7E1B) == 0) {
        xdata_write8(0x350C, xdata_read8(0x350C) | 0x02);
        call_unresolved(0xD792);
    }
    callback_low_54  = 0xDA;
    callback_high_55 = 0x9B;        /* callback/address value 9BDA */
}

/*
 * Suspend-like sequence at CODE C9AF (near strings "u2_go_suspend" and
 * "u2_exit_suspend"). Exact function/string association is unproven.
 * Observed bytes manipulate XDATA[0017].bit5, call helper routines, load CD/CD
 * into R6:R7 for a delay/service routine, then tail-jump to 9280.
 */
void suspend_like_sequence_C9AF(void)
{
    xdata_write8(0x0017, xdata_read8(0x0017) & 0xDF);
    call_unresolved(0xDF9E);
    xdata_write8(0x0017, xdata_read8(0x0017) | 0x20);
    call_unresolved(0xDE44);
    /* R6=0xCD; R7=0xCD; */
    call_unresolved(0xD76E);
    jump_unresolved(0x9280);
}

/*
 * Evidence-based diagnosis summary (not executable):
 * 1) Firmware contains status/debounce-like paths; it does not obviously contain
 *    an unconditional, visible USB-controller reset at VBUS return in these
 *    snippets.
 * 2) The observed callbacks branch on status bit7 and schedule follow-up work;
 *    stale suspend/debounce state or a timer/clock condition remains plausible.
 * 3) Since 9F59 and other calls enter zero-filled areas, the exact resume/reset
 *    behavior cannot be proven without the JMS565 bank/ROM map or a live trace.
 */
