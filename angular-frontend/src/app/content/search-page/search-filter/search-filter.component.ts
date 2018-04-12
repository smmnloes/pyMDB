import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-search-filter',
  templateUrl: './search-filter.component.html',
  styleUrls: ['./search-filter.component.css']
})
export class SearchFilterComponent implements OnInit {

  genreList = [];
  selectedGenres = [];
  dropdownSettings = {};

  constructor() {
  }

  ngOnInit() {
    this.genreList = [
      {"id": 1, "itemName": "India"},
      {"id": 2, "itemName": "Singapore"},
      {"id": 3, "itemName": "Australia"},
      {"id": 4, "itemName": "Canada"},
      {"id": 5, "itemName": "South Korea"},
      {"id": 6, "itemName": "Germany"},
      {"id": 7, "itemName": "France"},
      {"id": 8, "itemName": "Russia"},
      {"id": 9, "itemName": "Italy"},
      {"id": 10, "itemName": "Sweden"}
    ];
    this.selectedGenres = [];
    this.dropdownSettings = {
      singleSelection: false,
      text: "Select Genres (3 max)",
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      enableSearchFilter: true,
      classes: "myclass custom-class"
    };
  }

  onItemSelect(item: any) {

    if (this.selectedGenres.length > 3) {
      this.selectedGenres = [this.selectedGenres[0], this.selectedGenres[1], this.selectedGenres[2]];
    }
    console.log(item);
    console.log(this.selectedGenres);
  }

  onSelectAll(items: any) {
    this.selectedGenres = [this.selectedGenres[0], this.selectedGenres[1], this.selectedGenres[2]];
    console.log(this.selectedGenres);
  }
}
