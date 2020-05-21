import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {DetailedDataModel} from "../search-page/search-results/result/detailed-data-model";
import {BasicDataModel} from "../search-page/search-results/result/basic-data-model";
import {DetailService} from "../../../services/detail.service";
import {HttpClient} from "@angular/common/http";
import {QueryService} from "../../../services/query.service";
import {first} from "rxjs/operators";

@Component({
  selector: 'app-details-page',
  templateUrl: './details-page.component.html',
  styleUrls: ['./details-page.component.css']
})
export class DetailsPageComponent implements OnInit {
  movieId: number;
  detailedData: DetailedDataModel;
  basicData: BasicDataModel;

  constructor(private detailService: DetailService, private http: HttpClient, private activatedRoute: ActivatedRoute,
              private queryService: QueryService) {
    this.activatedRoute.params.subscribe(params => {
      this.movieId = params.movieId;
    });
  }

  ngOnInit() {
    this.detailService.getDetails(this.movieId).pipe(first()).subscribe(
      detailedData => this.detailedData = detailedData
    );

    this.queryService.getMovieById(this.movieId).pipe(first()).subscribe(
      basicData => this.basicData = basicData
    );
  }

}
