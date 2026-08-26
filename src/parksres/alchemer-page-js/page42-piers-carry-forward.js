let ppNames = `[question("value"), id="154"]`;
let ppCats  = `[question("value"), id="176"]`;
let wpNames = `[question("value"), id="159"]`;
let wpCats  = `[question("value"), id="177"]`;

const NAME_IDS = ['10326', '10327', '10328', '10329', '10330'];
const CAT_IDS  = ['10522', '10523', '10524', '10525', '10526'];

const NAME_PREFIX = '#sgE-391042299-42-117-';
const CAT_PREFIX  = '#sgE-391042299-42-180-';

function pairs(names, cats) {
  const n = names.split(",").map(s => s.trim()).filter(Boolean);
  const c = cats.split(",").map(s => s.trim());
  return n.map(function (name, i) {
    return { name: name, category: c[i] || "" };
  });
}

const selected = pairs(ppNames, ppCats)
  .concat(pairs(wpNames, wpCats))
  .slice(0, NAME_IDS.length);

$(document).ready(function () {
  console.log("[PAGE42] piers =", selected);

  selected.forEach(function (item, i) {
    $(NAME_PREFIX + NAME_IDS[i]).val(item.name).trigger('change');
    $(CAT_PREFIX + CAT_IDS[i]).val(item.category).trigger('change');

    const box = $('.piers .sg-input-checkbox')[i];
    if (box && !box.checked) box.click();
  });

  setTimeout(function () { $('.sg-next-button').click(); }, 300);
});
