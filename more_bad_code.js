function getProp(object, propertyName, defaultValue, anotherValue, subValue) {
  if (!object[propertyName]) {
    return defaultValue;
  }
  return object[propertyName];
}
const hero = {
  name: 'Batman',
  isVillian: false
};
console.log(getPropFixed(hero, 'isVillian', true)); // => false

