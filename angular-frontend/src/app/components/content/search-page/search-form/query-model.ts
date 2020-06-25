export class QueryModel {
  constructor(public director: string,
              public writer: string,
              public genres: string[],
              public min_rating_imdb: number,
              public year_from: number,
              public year_to: number,
              public principals: string[],
              public title: string,
              public results_per_page: number,
              public current_page: number,
              public sort_by: string
  ) {
  }

  public clone(): QueryModel {
    return new QueryModel(this.director, this.writer, Object.assign([], this.genres),
      this.min_rating_imdb, this.year_from, this.year_to, Object.assign([], this.principals),
      this.title, this.results_per_page, this.current_page, this.sort_by)
  }

  public static fromQueryParams(queryParams: any): QueryModel {
    return new QueryModel(
      queryParams['director'] == null ? "" : queryParams.director,
      queryParams['writer'] == null ? "" : queryParams.writer,
      this.getGenres(queryParams),
      queryParams['min_rating_imdb'] == null ? null : queryParams.min_rating_imdb,
      queryParams['year_from'] == null ? null : queryParams.year_from,
      queryParams['year_to'] == null ? null : queryParams.year_to,
      queryParams['principals'] == null ? ["", "", ""] : queryParams.principals,
      queryParams['title'] == null ? "" : queryParams.title,
      queryParams['results_per_page'] == null ? 15 : queryParams['results_per_page'],
      queryParams['current_page'] == null ? 1 : queryParams.current_page,
      queryParams['sort_by'] == null ? 'Relevance' : queryParams.sort_by
    );
  }

  private static getGenres(queryParams: any): string[] {
    if (typeof (queryParams['genres']) == "string") {
      return [queryParams['genres']];
    }

    return queryParams['genres'] == null ? null : queryParams['genres'];
  }


  public normalize(): string {
    let clonedModel = this.clone();
    clonedModel.current_page = -1;
    return JSON.stringify(clonedModel);
  }
}
