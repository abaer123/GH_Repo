# Create a javascript file to input a search criteria 
import Search from './Search';

const search = new Search();

search.on('submit', (criteria) => {
  // send search request with criteria
});

search.on('results', (results) => {
  // display results
})