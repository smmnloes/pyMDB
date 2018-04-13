import {Component, Input, OnInit} from '@angular/core';
import {SearchModel} from "./search-model";
import {QueryService} from "../../../query.service";

@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.css']
})
export class SearchFormComponent implements OnInit {
  searchModel: SearchModel;

  @Input()
  genres: string[];

  constructor(private queryService: QueryService) {
  }

  ngOnInit() {
    this.searchModel = new SearchModel("", "", [], null,
      null, null, ["", "", ""]);
  }

  onSubmit() {
    let result = this.queryService.makeQuery(this.searchModel);
    result.subscribe(data => {
        console.log(data)
      },
      err => console.error(err),
      () => console.log('SUCCESS!'))
  }

}
