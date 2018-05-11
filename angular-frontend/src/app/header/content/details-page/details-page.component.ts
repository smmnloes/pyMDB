import {Component, OnInit} from '@angular/core';
import {DetailService} from "../../../services/detail.service";
import {HttpClient} from "@angular/common/http";
import {Subject} from "rxjs/Subject";
import {ActivatedRoute} from "@angular/router";
import {DetailedDataModel} from "../search-page/search-results/result/detailed-data-model";
import {TMDB_API_KEY} from "../../../util/tmdb-api-key";

@Component({
  selector: 'app-details-page',
  templateUrl: './details-page.component.html',
  styleUrls: ['./details-page.component.css']
})
export class DetailsPageComponent implements OnInit {
  private movieId: number;
  private detailedData: DetailedDataModel;

  private fullPosterPathSource = new Subject<String>();
  private fullPosterPath$ = this.fullPosterPathSource.asObservable();

  constructor(private detailService: DetailService, private http: HttpClient, private activatedRoute: ActivatedRoute) {
    this.activatedRoute.params.subscribe(params => {
      this.movieId = params.movieId;
    });
  }

  ngOnInit() {
    this.detailService.detailedData$.subscribe(detailedData => {
      this.detailedData = detailedData;

      if (this.hasPosterPath()) {
        this.getFullPosterPath();
      }
    });

    if (this.movieId != null) {
      this.detailService.getDetails(this.movieId);
    } else {
      this.detailService.getCachedDetails();
    }


  }


  private hasPosterPath() {
    return this.detailedData != null && this.detailedData.posterPath != null;
  }


  /*
  Poster sizes:
   "w92",
   "w154",
   "w185",
   "w342",
   "w500",
   "w780",
   "original"
   */

  private getFullPosterPath() {
    this.http.get(this.detailService.TMDB_ROOT + 'configuration?api_key=' + TMDB_API_KEY)
      .subscribe(configData => {
          let baseUrl = configData['images']['base_url'];
          this.fullPosterPathSource.next(baseUrl + 'w185' + this.detailedData.posterPath);
        }
      );

  }

}
