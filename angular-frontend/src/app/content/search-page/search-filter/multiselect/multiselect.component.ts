import {Component, forwardRef, OnInit} from '@angular/core';
import {ControlValueAccessor, NG_VALUE_ACCESSOR} from "@angular/forms";

@Component({
  selector: 'app-multiselect',
  exportAs: 'multiselect',
  templateUrl: './multiselect.component.html',
  styleUrls: ['./multiselect.component.css'],

  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => MultiselectComponent),
      multi: true
    }
  ]
})
export class MultiselectComponent implements OnInit, ControlValueAccessor {
  genreList = [];
  selectedGenres = [];
  dropdownSettings = {};
  MAX_NUMBER_SELECTION = 3;

  propagateChange = (_: any) => {
  };

  writeValue(value: any) {
    this.selectedGenres = value;
  }

  registerOnChange(fn) {
    this.propagateChange = fn;
  }

  registerOnTouched() {
  }


  constructor() {
  }

  ngOnInit() {
    this.genreList = [{'itemName': 'Horror', 'id': 0},
      {'itemName': 'Music', 'id': 1},
      {'itemName': 'Documentary', 'id': 2},
      {'itemName': 'Film-Noir', 'id': 3},
      {'itemName': 'News', 'id': 4},
      {'itemName': 'Comedy', 'id': 5},
      {'itemName': 'Animation', 'id': 6},
      {'itemName': 'Sport', 'id': 7},
      {'itemName': 'Family', 'id': 8},
      {'itemName': 'Thriller', 'id': 9},
      {'itemName': 'History', 'id': 10},
      {'itemName': 'Mystery', 'id': 11},
      {'itemName': 'Game-Show', 'id': 12},
      {'itemName': 'War', 'id': 13},
      {'itemName': 'Romance', 'id': 14},
      {'itemName': 'Crime', 'id': 15},
      {'itemName': 'Short', 'id': 16},
      {'itemName': 'Fantasy', 'id': 17},
      {'itemName': 'Western', 'id': 18},
      {'itemName': 'Musical', 'id': 19},
      {'itemName': 'Sci-Fi', 'id': 20},
      {'itemName': 'Action', 'id': 21},
      {'itemName': 'Biography', 'id': 22},
      {'itemName': 'Adult', 'id': 23},
      {'itemName': 'Talk-Show', 'id': 24},
      {'itemName': 'Drama', 'id': 25},
      {'itemName': 'Adventure', 'id': 26},
      {'itemName': 'Reality-TV', 'id': 27},
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
    this.propagateChange(this.selectedGenres);
    console.log(item);
    console.log(this.selectedGenres);
  }

  onItemDeselect(item: any) {
    this.propagateChange(this.selectedGenres);
    console.log(item);
    console.log(this.selectedGenres);
  }

}
