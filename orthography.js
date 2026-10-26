/* Le tabelle sono inserite dal generatore a partire da hebrew_orthography.py. */
function createOrthography(spec) {
  'use strict';
  const letters = spec.letters;
  const reverse = {};
  for (const [ch, info] of Object.entries(letters)) {
    if (!(info.roman in reverse)) reverse[info.roman] = ch;
  }
  const nameKey = text => String(text).normalize('NFC').toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');
  const knownNames = new Map();
  const ambiguousNames = new Set();
  function registerName(name, hebrew) {
    const key = nameKey(name);
    const value = String(hebrew).normalize('NFC').split('').filter(ch => letters[ch]).join('');
    if (!key || !value || ambiguousNames.has(key)) return;
    if (knownNames.has(key) && knownNames.get(key) !== value) {
      knownNames.delete(key);
      ambiguousNames.add(key);
    } else knownNames.set(key, value);
  }
  for (const [name, hebrew] of Object.entries(spec.knownNames)) registerName(name, hebrew);

  function gematria(text, extendedFinals = false) {
    return Array.from(String(text)).reduce((sum, ch) => {
      const info = letters[ch];
      return sum + (info ? (extendedFinals ? (info.valFinal || info.val) : info.val) : 0);
    }, 0);
  }
  function numberToHebrew(number) {
    if (!Number.isSafeInteger(number) || number < 0) throw new RangeError('Serve un intero maggiore o uguale a zero.');
    let n = number;
    let result = 'ת'.repeat(Math.floor(n / 400));
    n %= 400;
    result += ['', 'ק', 'ר', 'ש'][Math.floor(n / 100)];
    n %= 100;
    if (n === 15) return result + 'טו';
    if (n === 16) return result + 'טז';
    return result + ['', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ'][Math.floor(n / 10)] + ['', 'א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט'][n % 10];
  }
  function transliterateHebrew(text) {
    return String(text).trim().split(/\s+/).map(word => Array.from(word).filter(ch => letters[ch]).map(ch => letters[ch].roman).join('·')).join(' / ');
  }
  const finalForms = {'כ':'ך', 'מ':'ם', 'נ':'ן', 'פ':'ף', 'צ':'ץ'};
  function finalize(word) {
    if (word.length < 2) return word;
    return word.slice(0, -1) + (finalForms[word.slice(-1)] || word.slice(-1));
  }
  const digraphs = {'sch':'ש', 'sh':'ש', 'ch':'ח', 'kh':'כ', 'th':'ת', 'tz':'צ', 'ts':'צ', 'ph':'פ'};
  const conventional = {'a':'א','b':'ב','c':'כ','d':'ד','e':'ה','f':'פ','g':'ג','h':'ה','i':'י','j':'י','k':'כ','l':'ל','m':'מ','n':'נ','o':'ו','p':'פ','q':'ק','r':'ר','s':'ס','t':'ת','u':'ו','v':'ו','w':'ו','x':'קס','y':'י','z':'ז'};
  function convertName(input) {
    const text = String(input).normalize('NFC').trim();
    // Un testo ebraico esplicito ha priorità sulla sua eventuale etichetta latina.
    if (Array.from(text).some(ch => letters[ch])) {
      const hebrew = text.replace(/[\u0591-\u05BD\u05BF-\u05C7]/g, '').split(/\s+/).map(word => Array.from(word).filter(ch => letters[ch]).join('')).filter(Boolean).join(' ');
      return {hebrew, kind:'hebrew'};
    }
    if (text.includes('·')) {
      const words = text.toLowerCase().split(/\s*\/\s*/);
      const parsed = words.map(word => word.split('·').map(token => reverse[token.trim()] || '').join(''));
      if (words.some(word => word.split('·').some(token => !reverse[token.trim()]))) return {hebrew:'', kind:'invalid'};
      return {hebrew:parsed.map(finalize).join(' '), kind:'transliteration'};
    }
    const key = nameKey(text);
    if (knownNames.has(key)) return {hebrew:knownNames.get(key), kind:'known'};
    if (ambiguousNames.has(key)) return {hebrew:'', kind:'ambiguous'};
    let allKnown = true;
    const words = text.split(/[\s/\-]+/).filter(Boolean).map(word => {
      if (knownNames.has(nameKey(word))) return knownNames.get(nameKey(word));
      allKnown = false;
      let result = '';
      const normalized = word.toLowerCase().normalize('NFC');
      for (let i = 0; i < normalized.length;) {
        const three = normalized.slice(i, i + 3);
        const two = normalized.slice(i, i + 2);
        if (digraphs[three]) { result += digraphs[three]; i += 3; }
        else if (digraphs[two]) { result += digraphs[two]; i += 2; }
        else {
          const ch = normalized[i++];
          const plain = ch.normalize('NFD').replace(/\p{M}/gu, '');
          result += reverse[ch] || conventional[plain] || '';
        }
      }
      return finalize(result);
    });
    return {hebrew:words.filter(Boolean).join(' '), kind:allKnown ? 'known' : 'conventional'};
  }
  function latinTokens(text) {
    const tokens = [];
    const input = String(text).normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();
    for (let i = 0; i < input.length;) {
      const explicit = input.slice(i).match(/^\[(hi|hv|i|v)\]/);
      if (explicit) {
        const token = explicit[1].toUpperCase();
        tokens.push({token:'[' + token + ']', value:spec.latinSpecial[token]});
        i += explicit[0].length;
      } else {
        const ch = input[i++];
        if (spec.latinValues[ch]) tokens.push({token:ch.toUpperCase(), value:spec.latinValues[ch]});
      }
    }
    return tokens;
  }
  function inlineText(value) {
    return String(value).replace(/\\/g, '\\\\').replace(/'/g, '\\x27').replace(/"/g, '\\x22')
      .replace(/&/g, '\\x26').replace(/</g, '\\x3c').replace(/>/g, '\\x3e')
      .replace(/\r/g, '\\r').replace(/\n/g, '\\n').replace(/\u2028/g, '\\u2028').replace(/\u2029/g, '\\u2029');
  }
  return {letters, registerName, gematria, numberToHebrew, transliterateHebrew, convertName,
          latinValues:spec.latinValues, latinTokens, inlineText,
          latinGematria:text => latinTokens(text).reduce((sum, item) => sum + item.value, 0)};
}
