import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-multiselect',
  templateUrl: './multiselect.component.html',
  styleUrls: ['./multiselect.component.css']
})
export class MultiselectComponent implements OnInit {

  genreList = [];
  selectedGenres = [];
  dropdownSettings = {};
  MAX_NUMBER_SELECTION = 3;

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
      text: `Select Genres (max. ${this.MAX_NUMBER_SELECTION})`,
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      enableSearchFilter: true,
      classes: "myclass custom-class",
      enableCheckAll: false
    };
  }


  onItemSelect(item: any) {
    if (this.selectedGenres.length > this.MAX_NUMBER_SELECTION) {
      let i = 0;
      let new_array = [];
      while (i < this.MAX_NUMBER_SELECTION) {
        new_array[i] = this.selectedGenres[i];
        i++;
      }
      this.selectedGenres = new_array;
    }
    console.log(item);
    console.log(this.selectedGenres);
  }

}
