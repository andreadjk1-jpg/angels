/* Calcoli geocentrici con Astronomy Engine; nomi derivati dalla tavola III.27. */
function createLunarEngine(astronomy, orthography, spec) {
  'use strict';
  const norm = value => {const remainder = value % 360; return remainder < 0 ? remainder + 360 : remainder;};
  const normalFinals = {'ך':'כ','ם':'מ','ן':'נ','ף':'פ','ץ':'צ'};
  const moonMap = Object.fromEntries(Array.from(spec.alphabet).map((ch, i) => [ch, spec.moonColumn[i]]));

  function instant(dateText, timeText, offsetHours) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(dateText) || !/^\d{2}:\d{2}(?::\d{2})?$/.test(timeText)) throw new Error('Inserisci data e ora complete.');
    const [year, month, day] = dateText.split('-').map(Number);
    const [hour, minute, second = 0] = timeText.split(':').map(Number);
    const offset = Number(offsetHours);
    if (year < 1 || year > 3000 || hour > 23 || minute > 59 || second > 59 || !Number.isFinite(offset) || offset < -14 || offset > 14) throw new Error('Data, ora o fuso fuori intervallo.');
    const wall = new Date(0);
    wall.setUTCFullYear(year, month - 1, day);
    wall.setUTCHours(hour, minute, second, 0);
    if (wall.getUTCFullYear() !== year || wall.getUTCMonth() !== month - 1 || wall.getUTCDate() !== day) throw new Error('La data indicata non esiste.');
    return new Date(wall.getTime() - offset * 3600000);
  }
  function mansionAt(longitude) {
    if (!Number.isFinite(longitude)) throw new Error('Longitudine lunare non valida.');
    const lon = norm(longitude);
    return spec.mansions.find(mansion => lon >= mansion.start && lon < mansion.end);
  }
  function phaseName(angle) {
    const a = norm(angle);
    const near = (value, target) => Math.abs(norm(value - target + 180) - 180) < 0.5;
    if (near(a, 0)) return 'Luna nuova · prossimità';
    if (near(a, 90)) return 'Primo quarto · prossimità';
    if (near(a, 180)) return 'Luna piena · prossimità';
    if (near(a, 270)) return 'Ultimo quarto · prossimità';
    return a < 90 ? 'Falce crescente' : a < 180 ? 'Gibbosa crescente' : a < 270 ? 'Gibbosa calante' : 'Falce calante';
  }
  function stateAt(date, options = {}) {
    if (!(date instanceof Date) || !Number.isFinite(date.getTime())) throw new Error('Istante UTC non valido.');
    const sun = astronomy.SunPosition(date);
    const moon = astronomy.EclipticGeoMoon(date);
    const phaseAngle = astronomy.MoonPhase(date);
    const illumination = astronomy.Illumination(astronomy.Body.Moon, date).phase_fraction;
    const shift = options.shift === undefined ? 0 : Number(options.shift);
    if (!Number.isFinite(shift)) throw new Error('Correzione zodiacale non valida.');
    const moonLongitude = norm(moon.lon + shift);
    const sunLongitude = norm(sun.elon + shift);
    const mansion = mansionAt(moonLongitude);
    return {utc:date.toISOString(), sunTropical:norm(sun.elon), moonTropical:norm(moon.lon),
      sunLongitude, moonLongitude, moonLatitude:moon.lat, distanceKm:moon.dist * 149597870.7,
      phaseAngle, illumination, phaseName:phaseName(phaseAngle), waxing:phaseAngle < 180,
      frame:options.frame || 'Tropicale', shift, mansion,
      suffix:options.suffix === 'יה' ? 'יה' : 'אל', offsetHours:Number(options.offsetHours || 0)};
  }
  function hierarchy(seed, suffix = 'אל', depth = 9) {
    if (!['אל','יה'].includes(suffix) || !Number.isInteger(depth) || depth < 1 || depth > 9) throw new Error('Suffisso o numero di gradi non valido.');
    let current = Array.from(String(seed)).map(ch => normalFinals[ch] || ch).filter(ch => moonMap[ch]).join('');
    if (!current) throw new Error('Inserisci un nome divino o angelico in ebraico, oppure un nome riconosciuto.');
    const result = [];
    for (let i = 0; i < depth; i++) {
      const steps = Array.from(current).map(ch => ({from:ch, to:moonMap[ch]}));
      const root = steps.map(step => step.to).join('');
      const hebrew = root + suffix;
      result.push({level:i + 1, order:spec.orders[i], seed:current, root_heb:root, hebrew,
        latin:orthography.transliterateHebrew(hebrew), gematria:orthography.gematria(hebrew), steps});
      current = hebrew;
    }
    return result;
  }
  return {norm, instant, mansionAt, phaseName, stateAt, hierarchy, spec};
}
