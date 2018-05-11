import {Component, OnInit} from '@angular/core';
import {QueryModel} from "./query-model";
import {QueryService} from "../../../../query.service";
import {ActivatedRoute, Router} from "@angular/router";


@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.css']
})
export class SearchFormComponent implements OnInit {

  private sortCriteria: string[] = ['Title', 'Year', 'Rating'];
  private queryModel: QueryModel;

  constructor(private queryService: QueryService, private router: Router, private activatedRoute: ActivatedRoute) {
  }

  ngOnInit() {
    this.activatedRoute.queryParams.subscribe(queryParams => {
        console.log(queryParams);
        this.queryModel = QueryModel.fromQueryParams(queryParams);
      }
    );
  }

  onSubmit() {
    console.log("onsubmit");
    console.log(this.queryModel);
    this.queryModel.current_page = 1;
    this.refetch();
  }

  onClickSortBy() {
    this.refetch();
  }

  refetch() {
       this.router.navigate(['/search'], {queryParams: JSON.parse(JSON.stringify(this.queryModel))});
  }

}
