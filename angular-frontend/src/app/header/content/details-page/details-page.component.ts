import {Component, OnInit} from '@angular/core';
import {DetailService} from "../../../services/detail.service";
import {HttpClient} from "@angular/common/http";
import {ActivatedRoute} from "@angular/router";
import {DetailedDataModel} from "../search-page/search-results/result/detailed-data-model";
import {BasicDataModel} from "../search-page/search-results/result/basic-data-model";
import {QueryService} from "../../../services/query.service";
import {first} from "rxjs/operators";

@Component({
  selector: 'app-details-page',
  templateUrl: './details-page.component.html',
  styleUrls: ['./details-page.component.css']
})
export class DetailsPageComponent implements OnInit {
  private movieId: number;
  detailedData: DetailedDataModel;
  basicData: BasicDataModel;

  fullPosterPath: string;

  constructor(private detailService: DetailService, private http: HttpClient, private activatedRoute: ActivatedRoute,
              private queryService: QueryService) {
    this.activatedRoute.params.subscribe(params => {
      this.movieId = params.movieId;
    });
  }

  ngOnInit() {
    this.detailService.detailedData$.pipe(first()).subscribe(detailedData => {
      this.detailedData = detailedData;

      if (this.hasPosterPath()) {
        this.detailService.getFullPosterPath(detailedData).pipe(first()).subscribe(path => this.fullPosterPath = path);
      }
    });

    this.detailService.getDetails(this.movieId);

    this.queryService.basicDataSingle$.pipe(first()).subscribe(basicData => {
      this.basicData = basicData;
    });

    this.queryService.getMovieById(this.movieId);

  }

  hasPosterPath(): boolean {
    return this.detailedData != null && this.detailedData.posterPath != null;
  }


}
