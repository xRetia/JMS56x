#!/usr/bin/env python3
"""Classic 8051/MCS-51 disassembler for a mapped JMS56x firmware code region."""
from pathlib import Path
from collections import deque, defaultdict
import argparse, re

LENGTH=[1]*256
for x in (0x01,0x11,0x21,0x31,0x41,0x51,0x61,0x71,0x81,0x91,0xA1,0xB1,0xC1,0xD1,0xE1,0xF1): LENGTH[x]=2
for x in (0x02,0x10,0x12,0x20,0x30,0x43,0x53,0x63,0x75,0x85,0x90,0xB4,0xB5,0xB6,0xB7,0xC0,0xD0,0xD5,0xE5,0xF5): LENGTH[x]=3
for x in (0x24,0x25,0x34,0x35,0x40,0x44,0x45,0x50,0x54,0x55,0x60,0x64,0x65,0x70,0x74,0x76,0x77,0x80,0x94,0x95,0xA6,0xA7,0xB2,0xB8,0xB9,0xBA,0xBB,0xBC,0xBD,0xBE,0xBF,0xC2,0xC5,0xD2,0xD6,0xD7,0xD8,0xD9,0xDA,0xDB,0xDC,0xDD,0xDE,0xDF): LENGTH[x]=2
for x in range(0x26,0x30): LENGTH[x]=1
for x in range(0x36,0x40): LENGTH[x]=1
for x in range(0x46,0x50): LENGTH[x]=1
for x in range(0x56,0x60): LENGTH[x]=1
for x in range(0x66,0x70): LENGTH[x]=1
for x in range(0x78,0x80): LENGTH[x]=2
for x in range(0x88,0x90): LENGTH[x]=2
for x in range(0x98,0xA0): LENGTH[x]=1
for x in range(0xA8,0xB0): LENGTH[x]=2
for x in range(0xE8,0xF0): LENGTH[x]=1
for x in range(0xF8,0x100): LENGTH[x]=1
# MOV direct,#imm, CJNE, etc lengths above are corrected by explicit groups.
LENGTH[0x75]=3; LENGTH[0x85]=3
for x in range(0xB8,0xC0): LENGTH[x]=3
LENGTH[0xB4]=LENGTH[0xB5]=LENGTH[0xB6]=LENGTH[0xB7]=3
LENGTH[0xD5]=3


def decode(c,pc):
 b=c[pc]; n=LENGTH[b]; u=lambda k:c[pc+k]
 r=f'R{b&7}'; ri=f'@R{b&1}'; d=lambda x:f'0x{x:02X}'; imm=lambda x:f'#0x{x:02X}'
 rel=lambda k:(pc+k+1+(u(k) if u(k)<128 else u(k)-256))&0xffff
 dptr=lambda:(u(1)<<8)|u(2)
 # AJMP/ACALL
 if b&0x1f in (0x01,0x11):
  t=((pc+2)&0xf800)|((b&0xe0)<<3)|u(1); call=(b&0x1f)==0x11
  return n,('ACALL' if call else 'AJMP')+f' 0x{t:04X}',('call' if call else 'jump'),([] if call else [t]),(t if call else None)
 if b in (0x02,0x12):
  t=dptr(); call=b==0x12
  return n,('LCALL' if call else 'LJMP')+f' 0x{t:04X}',('call' if call else 'jump'),([] if call else [t]),(t if call else None)
 if b==0xa5:return 1,'DB 0xA5 ; reserved/vendor opcode','next',[],None
 # instruction formats
 if b==0x00: op='NOP'
 elif b==0x03: op='RR A'
 elif b==0x04: op='INC A'
 elif b==0x05: op=f'INC {d(u(1))}'
 elif 0x06<=b<=0x07:op=f'INC {ri}'
 elif 0x08<=b<=0x0f:op=f'INC {r}'
 elif b==0x10:op=f'JBC {d(u(1))}, 0x{rel(2):04X}'
 elif b==0x13:op='RRC A'
 elif b==0x14:op='DEC A'
 elif b==0x15:op=f'DEC {d(u(1))}'
 elif 0x16<=b<=0x17:op=f'DEC {ri}'
 elif 0x18<=b<=0x1f:op=f'DEC {r}'
 elif b==0x20:op=f'JB {d(u(1))}, 0x{rel(2):04X}'
 elif b==0x22:op='RET'
 elif b==0x23:op='RL A'
 elif b in (0x24,0x25):op=f'ADD A, {imm(u(1)) if b==0x24 else d(u(1))}'
 elif 0x26<=b<=0x27:op=f'ADD A, {ri}'
 elif 0x28<=b<=0x2f:op=f'ADD A, {r}'
 elif b==0x30:op=f'JNB {d(u(1))}, 0x{rel(2):04X}'
 elif b==0x32:op='RETI'
 elif b==0x33:op='RLC A'
 elif b in (0x34,0x35):op=f'ADDC A, {imm(u(1)) if b==0x34 else d(u(1))}'
 elif 0x36<=b<=0x37:op=f'ADDC A, {ri}'
 elif 0x38<=b<=0x3f:op=f'ADDC A, {r}'
 elif b in (0x40,0x50,0x60,0x70,0x80):
  nm={0x40:'JC',0x50:'JNC',0x60:'JZ',0x70:'JNZ',0x80:'SJMP'}[b];op=f'{nm} 0x{rel(1):04X}'
 elif b==0x42:op=f'ORL {d(u(1))}, A'
 elif b==0x43:op=f'ORL {d(u(1))}, {imm(u(2))}'
 elif b in (0x44,0x45):op=f'ORL A, {imm(u(1)) if b==0x44 else d(u(1))}'
 elif 0x46<=b<=0x47:op=f'ORL A, {ri}'
 elif 0x48<=b<=0x4f:op=f'ORL A, {r}'
 elif b==0x52:op=f'ANL {d(u(1))}, A'
 elif b==0x53:op=f'ANL {d(u(1))}, {imm(u(2))}'
 elif b in (0x54,0x55):op=f'ANL A, {imm(u(1)) if b==0x54 else d(u(1))}'
 elif 0x56<=b<=0x57:op=f'ANL A, {ri}'
 elif 0x58<=b<=0x5f:op=f'ANL A, {r}'
 elif b==0x62:op=f'XRL {d(u(1))}, A'
 elif b==0x63:op=f'XRL {d(u(1))}, {imm(u(2))}'
 elif b in (0x64,0x65):op=f'XRL A, {imm(u(1)) if b==0x64 else d(u(1))}'
 elif 0x66<=b<=0x67:op=f'XRL A, {ri}'
 elif 0x68<=b<=0x6f:op=f'XRL A, {r}'
 elif b==0x72:op=f'ORL C, {d(u(1))}'
 elif b==0x73:op='JMP @A+DPTR'
 elif b==0x74:op=f'MOV A, {imm(u(1))}'
 elif b==0x75:op=f'MOV {d(u(1))}, {imm(u(2))}'
 elif 0x76<=b<=0x77:op=f'MOV {ri}, {imm(u(1))}'
 elif 0x78<=b<=0x7f:op=f'MOV {r}, {imm(u(1))}'
 elif b==0x82:op=f'ANL C, {d(u(1))}'
 elif b==0x83:op='MOVC A, @A+PC'
 elif b==0x84:op='DIV AB'
 elif b==0x85:op=f'MOV {d(u(2))}, {d(u(1))}'
 elif b in (0x86,0x87):op=f'MOV {d(u(1))}, @R{b&1}'
 elif 0x88<=b<=0x8f:op=f'MOV {d(u(1))}, {r}'
 elif b==0x90:op=f'MOV DPTR, #0x{dptr():04X}'
 elif b==0x92:op=f'MOV {d(u(1))}, C'
 elif b==0x93:op='MOVC A, @A+DPTR'
 elif b==0x94:op=f'SUBB A, {imm(u(1))}'
 elif b==0x95:op=f'SUBB A, {d(u(1))}'
 elif 0x96<=b<=0x97:op=f'SUBB A, {ri}'
 elif 0x98<=b<=0x9f:op=f'SUBB A, {r}'
 elif b==0xa0:op=f'ANL C, /{d(u(1))}'
 elif b==0xa2:op=f'MOV C, {d(u(1))}'
 elif b==0xa3:op='INC DPTR'
 elif b==0xa4:op='MUL AB'
 elif b in (0xa6,0xa7):op=f'MOV @R{b&1}, {d(u(1))}'
 elif 0xa8<=b<=0xaf:op=f'MOV {r}, {d(u(1))}'
 elif b==0xb0:op=f'ANL C, /{d(u(1))}'
 elif b==0xb2:op=f'CPL {d(u(1))}'
 elif b==0xb3:op='CPL C'
 elif b==0xb4:op=f'CJNE A, {imm(u(1))}, 0x{rel(2):04X}'
 elif b==0xb5:op=f'CJNE A, {d(u(1))}, 0x{rel(2):04X}'
 elif b in (0xb6,0xb7):op=f'CJNE @R{b&1}, {imm(u(1))}, 0x{rel(2):04X}'
 elif 0xb8<=b<=0xbf:op=f'CJNE {r}, {imm(u(1))}, 0x{rel(2):04X}'
 elif b==0xc0:op=f'PUSH {d(u(1))}'
 elif b==0xc2:op=f'CLR {d(u(1))}'
 elif b==0xc3:op='CLR C'
 elif b==0xc4:op='SWAP A'
 elif b==0xc5:op=f'XCH A, {d(u(1))}'
 elif b in (0xc6,0xc7):op=f'XCH A, @R{b&1}'
 elif 0xc8<=b<=0xcf:op=f'XCH A, {r}'
 elif b==0xd0:op=f'POP {d(u(1))}'
 elif b==0xd2:op=f'SETB {d(u(1))}'
 elif b==0xd3:op='SETB C'
 elif b==0xd4:op='DA A'
 elif b==0xd5:op=f'DJNZ {d(u(1))}, 0x{rel(2):04X}'
 elif b in (0xd6,0xd7):op=f'XCHD A, @R{b&1}'
 elif 0xd8<=b<=0xdf:op=f'DJNZ {r}, 0x{rel(1):04X}'
 elif b==0xe0:op='MOVX A, @DPTR'
 elif b in (0xe2,0xe3):op=f'MOVX A, @R{b&1}'
 elif b==0xe4:op='CLR A'
 elif b==0xe5:op=f'MOV A, {d(u(1))}'
 elif b in (0xe6,0xe7):op=f'MOV A, @R{b&1}'
 elif 0xe8<=b<=0xef:op=f'MOV A, {r}'
 elif b==0xf0:op='MOVX @DPTR, A'
 elif b in (0xf2,0xf3):op=f'MOVX @R{b&1}, A'
 elif b==0xf4:op='CPL A'
 elif b==0xf5:op=f'MOV {d(u(1))}, A'
 elif b in (0xf6,0xf7):op=f'MOV @R{b&1}, A'
 elif 0xf8<=b<=0xff:op=f'MOV {r}, A'
 else:op=f'DB 0x{b:02X}'
 # control-flow metadata
 kind='next'; targets=[]; call=None
 if b in (0x02,):kind='jump';targets=[dptr()]
 elif b==0x12:kind='call';call=dptr()
 elif b&0x1f==0x01:kind='jump';targets=[((pc+2)&0xf800)|((b&0xe0)<<3)|u(1)]
 elif b&0x1f==0x11:kind='call';call=((pc+2)&0xf800)|((b&0xe0)<<3)|u(1)
 elif b in (0x22,0x32):kind='ret'
 elif b==0x73:kind='indirect'
 elif b==0x80:kind='jump';targets=[rel(1)]
 elif b in (0x10,0x20,0x30,0x40,0x50,0x60,0x70,0xb4,0xb5,0xb6,0xb7,0xd5) or 0xb8<=b<=0xbf or 0xd8<=b<=0xdf:
  kind='cond';targets=[rel(2 if b in (0x10,0x20,0x30,0xb4,0xb5,0xb6,0xb7,0xd5) or 0xb8<=b<=0xbf else 1)]
 return n,op,kind,targets,call


def control_flow(code,seeds):
 # Large zero-filled spans are treated as unmapped/padding/ROM-bank holes.
 # Without the chip's bank map it would be unsafe to execute through them as NOPs.
 holes=set(); i=0
 while i<len(code):
  if code[i]!=0: i+=1; continue
  j=i+1
  while j<len(code) and code[j]==0: j+=1
  if j-i>=64: holes.update(range(i,j))
  i=j
 seen={};q=deque(seeds); unresolved=set()
 while q:
  pc=q.popleft()
  if not 0<=pc<len(code) or pc in seen:continue
  if pc in holes:
   unresolved.add(pc); continue
  n,mn,kind,targets,call=decode(code,pc);seen[pc]=(n,mn,kind,targets,call)
  if call is not None:q.append(call)
  q.extend(targets)
  if kind in ('next','cond','call') and pc+n<len(code):q.append(pc+n)
 return seen,unresolved

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--outdir',required=True);ap.add_argument('--file-base',type=lambda x:int(x,0),default=0x10000);ap.add_argument('--code-size',type=lambda x:int(x,0),default=0xe000);a=ap.parse_args()
 blob=Path(a.input).read_bytes();code=blob[a.file_base:a.file_base+a.code_size];out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
 reach,unresolved=control_flow(code,[0,3,0xb,0x13,0x1b,0x23,0x2b])
 p=out/'JMS565_full_linear_disassembly.lst'
 with p.open('w') as f:
  f.write(f'; Classic 8051 linear sweep; file offset = 0x{a.file_base:06X} + CPU address; image code size={len(code)} bytes.\n; R marks instruction starts reached by a simple 8051 control-flow walk seeded by reset and standard vectors.\n; Linear sweep includes constants/data, which are necessarily disassembled as instructions.\n; CPU range 0000-DFFF maps to file 010000-01DFFF.\n')
  pc=0
  while pc<len(code):
   n,op,*_=decode(code,pc);n=max(1,min(n,len(code)-pc));mark='R' if pc in reach else '.'
   f.write(f'{pc:04X} [{a.file_base+pc:06X}] {mark} {code[pc:pc+n].hex(" ").upper():<9} {op}\n');pc+=n
 with (out/'JMS565_reachable_disassembly.lst').open('w') as f:
  f.write('; Reachability from reset and conventional interrupt vector entries; approximate.\n')
  for pc,(n,op,*_) in sorted(reach.items()):f.write(f'{pc:04X} [{a.file_base+pc:06X}] {code[pc:pc+n].hex(" ").upper():<9} {op}\n')
 calls=defaultdict(list)
 for pc,(n,op,k,t,c) in reach.items():
  if c is not None:calls[c].append(pc)
 with (out/'JMS565_control_flow_summary.txt').open('w') as f:
  f.write(f'File SHA256: {__import__("hashlib").sha256(blob).hexdigest()}\nCode range: file 0x{a.file_base:06X}-0x{a.file_base+len(code)-1:06X} mapped to CPU 0000-DFFF.\nReachable instruction starts: {len(reach)}; direct calls seen: {sum(map(len,calls.values()))}.\nLong zero-filled targets (>=64 bytes contiguous) are treated as unresolved holes, not executable NOP code.\n\nCALL TARGET <- CALLERS\n')
  for t,srcs in sorted(calls.items()):f.write(f'{t:04X} <- '+', '.join(f'{x:04X}' for x in sorted(srcs))+'\n')
  f.write('\nUnresolved control-flow targets entering long zero-filled spans:\n')
  for t in sorted(unresolved):f.write(f'{t:04X} file=0x{a.file_base+t:06X} bytes={code[t:t+8].hex(" ")}\n')
  f.write('\nASCII strings in code region:\n')
  for m in re.finditer(rb'[\x20-\x7e]{5,}',code):f.write(f'{m.start():04X}: {m.group().decode(errors="replace")}\n')
 print('reachable instruction starts',len(reach),'direct calls',sum(map(len,calls.values())),'unresolved hole targets',len(unresolved))
 for name in ['JMS565_full_linear_disassembly.lst','JMS565_reachable_disassembly.lst','JMS565_control_flow_summary.txt']:
  q=out/name;print(q,q.stat().st_size)
if __name__=='__main__':main()
