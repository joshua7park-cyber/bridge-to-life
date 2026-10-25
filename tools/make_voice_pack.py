#!/usr/bin/env python3
"""
생명의 다리 — AI 음성 팩 만들기 (Mac)

언어 파일(lang/xx.json)의 모든 문장을 AI 음성으로 미리 녹음해서
앱의 [설정 › AI 음성 팩 받기]에서 받을 수 있는 음성 팩을 만듭니다.

사용법 (이 파일이 있는 BridgeToLife_PWA 폴더에서 터미널로):
  # 1) Mac 내장 고품질 음성 (인터넷 불필요, 기본값)
  python3 tools/make_voice_pack.py ko --voice "Yuna (Premium)" --name "유나 (AI 고품질)"

  # 2) Microsoft 신경망 음성 (인터넷 필요: pip3 install edge-tts)
  python3 tools/make_voice_pack.py ko --engine edge --voice ko-KR-SunHiNeural --name "선희 (AI)"

  사용 가능한 Mac 음성 보기:  say -v '?'
  Mac 고품질 음성 받기: 시스템 설정 › 손쉬운 사용 › 읽기 및 말하기 › 시스템 음성 › 음성 관리

추천 음성
  ko  Mac: Yuna (Premium)      edge: ko-KR-SunHiNeural / ko-KR-InJoonNeural
  en  Mac: Ava (Premium)       edge: en-US-AvaNeural / en-US-AndrewNeural
  ja  Mac: Kyoko (Enhanced)    edge: ja-JP-NanamiNeural / ja-JP-KeitaNeural
  zh-CN Mac: Tingting (Enhanced) edge: zh-CN-XiaoxiaoNeural / zh-CN-YunxiNeural
  id  Mac: Damayanti (Enhanced)  edge: id-ID-GadisNeural / id-ID-ArdiNeural
  es  Mac: Mónica (Enhanced)   edge: es-ES-ElviraNeural / es-MX-DaliaNeural

결과: voice/<id>/pack.json + 음성 파일, voice/index.json 목록에 자동 추가.
폴더 전체를 서버에 다시 올리면 앱에서 바로 받을 수 있습니다.
※ 언어 파일의 문장을 고치면 음성 팩도 다시 만들어야 합니다(--version 숫자를 올리세요).
※ 만든 음성을 공개 배포할 때는 사용한 음성 엔진의 이용 약관을 확인하세요.
"""
import argparse, asyncio, json, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def items_for(pack):
    """앱이 읽는 순서와 똑같이 단계별 문장 목록을 만든다 (key = '단계-순번')."""
    out = []
    ui = pack.get('ui', {})
    for si, s in enumerate(pack['steps']):
        seq = [s['title']]
        for v in s.get('verses', []):
            seq.append((v['text'] + ' ' + (v.get('say') or v.get('ref') or '')).strip())
        seq += list(s.get('body', []))
        if s.get('prayer'):
            seq.append(s['prayer'])
        if s.get('list'):
            seq.append(ui.get('growth', 'Growing in your new life'))
            seq += list(s['list'])
        for ii, text in enumerate(seq):
            out.append((f'{si}-{ii}', text))
    return out


def mac_say(text, voice, rate, out_path):
    tmp = out_path + '.aiff'
    cmd = ['say', '-v', voice, '-o', tmp]
    if rate:
        cmd += ['-r', str(rate)]
    cmd += ['--', text]
    subprocess.run(cmd, check=True)
    subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', '-b', '64000', tmp, out_path], check=True)
    os.remove(tmp)


async def edge_say(text, voice, rate, out_path):
    import edge_tts  # pip3 install edge-tts
    kw = {}
    if rate:
        kw['rate'] = rate  # 예: "-10%"
    await edge_tts.Communicate(text, voice, **kw).save(out_path)


def main():
    ap = argparse.ArgumentParser(description='생명의 다리 AI 음성 팩 만들기')
    ap.add_argument('lang', help='언어 코드 (lang 폴더의 파일 이름, 예: ko, en, ja, zh-CN, id, es)')
    ap.add_argument('--engine', choices=['mac', 'edge'], default='mac')
    ap.add_argument('--voice', required=True, help='음성 이름')
    ap.add_argument('--name', help='앱에 보일 이름')
    ap.add_argument('--id', help='음성 팩 ID (영문·숫자, 기본: 언어-음성)')
    ap.add_argument('--desc', default='', help='짧은 설명')
    ap.add_argument('--rate', default='', help='mac: 분당 단어 수(예 170) / edge: "-10%" 같은 비율')
    ap.add_argument('--version', type=int, default=1)
    a = ap.parse_args()

    lang_path = os.path.join(ROOT, 'lang', a.lang + '.json')
    if not os.path.exists(lang_path):
        sys.exit(f'언어 파일이 없습니다: {lang_path}')
    pack = json.load(open(lang_path, encoding='utf-8'))
    code = pack['meta']['code']
    vid = a.id or re.sub(r'[^\w.\-]+', '-', f"{code}-{a.voice}".lower()).strip('-')[:60]
    out_dir = os.path.join(ROOT, 'voice', vid)
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir)

    ext = 'm4a' if a.engine == 'mac' else 'mp3'
    items = items_for(pack)
    files = {}
    for n, (key, text) in enumerate(items, 1):
        fname = f'{key}.{ext}'
        path = os.path.join(out_dir, fname)
        print(f'[{n}/{len(items)}] {key}  {text[:40]}…')
        if a.engine == 'mac':
            mac_say(text, a.voice, a.rate, path)
        else:
            asyncio.run(edge_say(text, a.voice, a.rate, path))
        files[key] = fname

    meta = {
        'id': vid, 'lang': code, 'name': a.name or a.voice, 'desc': a.desc or a.voice,
        'engine': a.engine, 'voice': a.voice, 'version': a.version,
        'langVersion': pack['meta'].get('version', 1), 'files': files,
    }
    json.dump(meta, open(os.path.join(out_dir, 'pack.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    size = sum(os.path.getsize(os.path.join(out_dir, f)) for f in os.listdir(out_dir))
    idx_path = os.path.join(ROOT, 'voice', 'index.json')
    idx = json.load(open(idx_path, encoding='utf-8')) if os.path.exists(idx_path) else {'voices': []}
    idx['voices'] = [v for v in idx.get('voices', []) if v.get('id') != vid]
    idx['voices'].append({'id': vid, 'lang': code, 'name': meta['name'], 'desc': meta['desc'],
                          'size': f'{size / 1048576:.1f} MB', 'version': a.version, 'pack': f'{vid}/pack.json'})
    json.dump(idx, open(idx_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'\n완료: voice/{vid}/ ({len(files)}개 파일, {size / 1048576:.1f} MB) — voice/index.json에 추가했습니다.')


if __name__ == '__main__':
    main()
