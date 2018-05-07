import {Component, OnInit} from '@angular/core';
import {DetailService} from "../../../detail.service";
import {HttpClient} from "@angular/common/http";
import {Subject} from "rxjs/Subject";
import {ActivatedRoute} from "@angular/router";
import {DetailedDataModel} from "../search-page/search-results/result/detailed-data-model";

@Component({
  selector: 'app-details-page',
  templateUrl: './details-page.component.html',
  styleUrls: ['./details-page.component.css']
})
export class DetailsPageComponent implements OnInit {
  private id: number;
  private detailedData: DetailedDataModel;

  private fullPosterPathSource = new Subject<String>();
  private fullPosterPath$ = this.fullPosterPathSource.asObservable();

  constructor(private detailService: DetailService, private http: HttpClient, private activatedRoute: ActivatedRoute) {
    this.activatedRoute.params.subscribe(params => {
      this.id = params.id;
    });
  }

  ngOnInit() {
    this.detailService.detailedData$.subscribe(detailedData => {
      this.detailedData = detailedData;

      console.log(detailedData);
      if (this.hasPosterPath()) {
        this.getFullPosterPath();
      }
    });

    if (this.id != null) {
      this.detailService.getDetails(this.id);
    } else {
      this.detailService.getLastDetails();
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
    return this.http.get(this.detailService.TMDB_ROOT + 'configuration?api_key=' + this.detailService.TMDB_API_KEY).subscribe(configData => {
        let baseUrl = configData['images']['base_url'];
        this.fullPosterPathSource.next(baseUrl + 'w185' + this.detailedData.posterPath);
      }
    );

  }

}
