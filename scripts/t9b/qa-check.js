(() => {
  const t = document.body.innerText;
  const has = (s) => t.includes(s);
  const checks = {};
  // section titles
  checks['sec 9.9 title'] = has('Reversible Reactions and Dynamic Equilibrium');
  checks['sec 9.10 title'] = has('Changing Conditions and the Position of Equilibrium');
  checks['sec 9.11 title'] = has('Reversible Reactions in Industry');
  // spec map rows
  checks['map 9.9 statement'] = has('the rate of the forward reaction is equal to the rate of the backward reaction');
  checks['map 9.10 statement'] = has('changes of temperature, pressure and concentration on the position of equilibrium');
  checks['map 9.11 statement'] = has('compromise between the yield and the rate of reaction');
  checks['map practical 9B'] = has('iodine(I) chloride');
  checks['two-parts note updated'] = has('9A Kinetics') && has('9B Equilibria') && !has('next part');
  // 9.9 content
  checks['irreversible H2+O2'] = has('no uncombined hydrogen and oxygen is left');
  checks['HI 90%'] = has('only about 90% of hydrogen and iodine reacts');
  checks['CaCO3 closed vessel'] = has('only a small portion of CaCO₃ decomposes');
  checks['forward vs backward'] = has('forward reaction') && has('reverse (backward) reaction');
  checks['equilibrium reached'] = has('At this point a dynamic equilibrium has been reached');
  checks['two conditions'] = has('The reaction mixture must be in a closed container');
  checks['three features'] = has('The reactions continue to occur in both directions');
  // 9.10 content
  checks['homogeneous eq'] = has('Homogeneous equilibrium');
  checks['heterogeneous eq'] = has('Heterogeneous equilibrium');
  checks['ester eq'] = has('CH₃COOCH₂CH₃(l)') && has('H₂O(l)');
  checks['Cu Ag balance'] = has('2Ag⁺(aq)') && has('Cu²⁺(aq)');
  checks['chromate example'] = has('chromate(VI)') && has('dichromate(VI)');
  checks['acid orange'] = has('equilibrium moves to the right and solution becomes orange');
  checks['four factors'] = has('Addition of a catalyst');
  checks['conc summary'] = has('Reactants increase') && has('Products decrease');
  checks['pressure no-effect'] = has('changes of pressure have no effect on the composition of equilibrium mixture');
  checks['moles captions'] = has('2 moles ⇌ 2 moles') && has('3 moles ⇌ 2 moles') && has('4 moles ⇌ 2 moles');
  checks['pressure summary'] = has('Moves to side with fewer gaseous molecules');
  checks['temp endothermic'] = has('shifts towards the endothermic direction');
  checks['temp summary'] = has('Moves to LEFT') && has('Moves to RIGHT');
  checks['catalyst NO EFFECT'] = has('NO EFFECT');
  checks['key point box'] = has('equilibrium is reached sooner than without catalyst');
  checks['limitations'] = has('The arguments are not explanations of why changes sometimes occur');
  checks['NO2 example'] = has('beaker of hot water') && has('−57.2 kJ mol⁻¹');
  checks['darker colour verdict'] = has('the temperature effect must be greater than the pressure effect');
  // 9.11 content
  checks['compromise conditions'] = has('compromise conditions');
  checks['haber eq dH'] = has('−92.4 kJ mol⁻¹');
  checks['why 450'] = has('Why are conditions of 450 °C and 250 atm used?');
  checks['NN bond'] = has('E(N≡N) = 945 kJ mol⁻¹');
  checks['iron catalyst'] = has('so iron is used in the industrial process');
  checks['products removed'] = has('products are removed from the system as they are formed');
  checks['haber conditions'] = has('250 atm');
  checks['contact eq'] = has('−96 kJ mol⁻¹') && has('½O₂(g)');
  checks['97 percent'] = has('very high at 97%');
  checks['V2O5 mechanism'] = has('V₂O₅(s)') && has('V₂O₄(s)');
  checks['contact conditions'] = has('2 atm');
  // stale content must be gone
  checks['no Le Chatelier'] = !has('Le Chatelier');
  checks['no CHECKPOINT'] = !has('CHECKPOINT');
  checks['no EXERCISE'] = !has('EXERCISE');
  // figures present in DOM
  const imgs = [...document.querySelectorAll('img[src*="/diagrams/eq-"]')];
  checks['eq figures in DOM (6)'] = imgs.length === 6;
  const broken = imgs.filter((i) => i.complete && i.naturalWidth === 0);
  checks['no broken eq figures'] = broken.length === 0;
  return JSON.stringify({ fail: Object.entries(checks).filter(([, v]) => !v).map(([k]) => k), total: Object.keys(checks).length, imgs: imgs.length });
})()
