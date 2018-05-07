import {Component, Input, OnInit} from '@angular/core';
import {QueryModel} from "./query-model";
import {QueryService} from "../../../../query.service";


@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.css']
})
export class SearchFormComponent implements OnInit {
  queryModel: QueryModel;

  private sortCriteria: string[];


  @Input()
  genres: string[];

  constructor(private queryService: QueryService) {
    this.sortCriteria = [
      'Title', 'Year', 'Rating'
    ];

  }

  ngOnInit() {

    let lastQuery = this.queryService.getLastQuery();
    if (lastQuery != null) {
      this.queryModel = lastQuery;
      this.queryService.makeQuery(lastQuery, true);
    } else {
      this.queryModel = new QueryModel("", "", [], null,
        null, null, ["", "", ""], "", null, 1, this.sortCriteria[0]);
    }
  }

  onSubmit() {
    this.queryService.makeQuery(this.queryModel, true);
  }


  onClickSortBy() {
    if (this.queryService.lastQuery != null) {
      this.queryService.changeSortBy(this.queryModel.sort_by);
    }
  }

}
